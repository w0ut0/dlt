const proc = require('child_process')
const fs = require('fs');
const semver = require('semver')


// const
REPO_DIR = ".dlt-repo"
REPO_DOCS_DIR = REPO_DIR + "/docs/website"
REPO_URL = "https://github.com/dlt-hub/dlt.git"
VERSIONED_DOCS_FOLDER = "versioned_docs"
VERSIONED_SIDEBARS_FOLDER = "versioned_sidebars"

// no doc versions below this version will be deployed
MINIMUM_SEMVER_VERSION = "0.4.0"

// clear old repo version
fs.rmSync(REPO_DIR, { recursive: true, force: true })

// checkout fresh
console.log("Checking out dlt repo")
proc.execSync(`git clone ${REPO_URL} ${REPO_DIR}`)

// find tags
console.log("Discovering versions")
const tags = proc.execSync(`cd ${REPO_DIR} && git tag`).toString().trim().split("\n");
console.log(`Found ${tags.length} tags`)

// parse and filter invalid tags
let versions = tags.map(v => semver.valid(v)).filter(v => v != null)

// remove all tags below the min version and sort
min_version = semver.valid(MINIMUM_SEMVER_VERSION)
versions = semver.rsort(versions.filter(v => semver.gt(v, min_version)))

// remove prelease versions
versions.filter(v => semver.prerelease(v) == null)

console.log(`Found ${versions.length} elligible versions`)
if (versions.length < 5) {
    console.error("Sanity check failed, not enough elligble version tags found")
    process.exit(1)
}

// go through the versions and find all newest versions of minor versions
const selectedVersions = ["master"];
let lastVersion = versions[0];
for (let ver of versions) {
    if (semver.minor(ver) != semver.minor(lastVersion) || semver.major(ver) != semver.major(lastVersion)) {
        selectedVersions.push(ver)
    }
    lastVersion = ver;
}

console.log(`Will create docs versions for ${selectedVersions}`)

// create folders
fs.rmSync(VERSIONED_DOCS_FOLDER, { recursive: true, force: true })
fs.rmSync(VERSIONED_SIDEBARS_FOLDER, { recursive: true, force: true })
fs.rmSync("versions.json", { force: true })

fs.mkdirSync(VERSIONED_DOCS_FOLDER);
fs.mkdirSync(VERSIONED_SIDEBARS_FOLDER);

// check that checked out repo is on devel
console.log("Checking branch")
const branch = proc.execSync(`cd ${REPO_DIR} && git rev-parse --abbrev-ref HEAD`).toString().trim()

if (branch != "devel") {
    console.error("Could not check out devel branch")
    process.exit(1)
}

selectedVersions.reverse()
for (const version of selectedVersions) {

    // checkout verison and verify we have the right tag
    console.log(`Generating version ${version}, switching to tag:`)
    proc.execSync(`cd ${REPO_DIR} && git checkout ${version}`)

    // const tag = proc.execSync(`cd ${REPO_DIR} && git describe --exact-match --tags`).toString().trim()
    // if (tag != version) {
    //     console.error(`Could not checkout version ${version}`)
    //     process.exit(1)
    // }

    // build doc version, we also run preprocessing and markdown gen for each doc version
    console.log(`Building docs...`)
    proc.execSync(`cd ${REPO_DOCS_DIR} && npm run preprocess-docs && PYTHONPATH=. pydoc-markdown`)

    console.log(`Snapshotting version...`)
    proc.execSync(`cd ${REPO_DOCS_DIR} && npm run docusaurus docs:version ${version}`)

    console.log(`Moving snapshot`)
    fs.cpSync(REPO_DOCS_DIR+"/"+VERSIONED_DOCS_FOLDER, VERSIONED_DOCS_FOLDER, {recursive: true})
    fs.cpSync(REPO_DOCS_DIR+"/"+VERSIONED_SIDEBARS_FOLDER, VERSIONED_SIDEBARS_FOLDER, {recursive: true})   
 
}

fs.cpSync(REPO_DOCS_DIR+"/versions.json", "versions.json")
