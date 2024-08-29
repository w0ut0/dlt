const proc = require('child_process')
const fs = require('fs');

// const
REPO_DIR = ".dlt-repo"
REPO_DOCS_DIR = REPO_DIR + "/docs/website"
REPO_URL = "https://github.com/dlt-hub/dlt.git"
VERSIONED_DOCS_FOLDER = "versioned_docs"
VERSIONED_SIDEBARS_FOLDER = "versioned_sidebars"

// TODO: get tags automatically, put newest version on top
const VERSIONS = [
    "0.5.4",
    "0.4.12",
]

// create folders
fs.rmSync(VERSIONED_DOCS_FOLDER, { recursive: true, force: true })
fs.rmSync(VERSIONED_SIDEBARS_FOLDER, { recursive: true, force: true })
fs.rmSync("versions.json", { force: true })

fs.mkdirSync(VERSIONED_DOCS_FOLDER);
fs.mkdirSync(VERSIONED_SIDEBARS_FOLDER);

// clear old repo version
fs.rmSync(REPO_DIR, { recursive: true, force: true })

// checkout fresh
console.log("Checking out dlt repo")
proc.execSync(`git clone ${REPO_URL} ${REPO_DIR}`)

// check that checked out repo is on devel
console.log("Checking branch")
const branch = proc.execSync(`cd ${REPO_DIR} && git rev-parse --abbrev-ref HEAD`).toString().trim()

if (branch != "devel") {
    console.error("Could not check out devel branch")
    process.exit()
}

VERSIONS.reverse()
for (const version of VERSIONS) {

    // checkout verison and verify we have the right tag
    console.log(`Generating version ${version}, switching to tag:`)
    proc.execSync(`cd ${REPO_DIR} && git checkout ${version}`)
    const tag = proc.execSync(`cd ${REPO_DIR} && git describe --exact-match --tags`).toString().trim()
    if (tag != version) {
        console.error(`Could not checkout version ${version}`)
        process.exit()
    }

    // build doc version, we also run preprocessing and markdown gen for each doc version
    console.log(`Building docs...`)
    proc.execSync(`cd ${REPO_DOCS_DIR} && node tools/preprocess_docs.js && PYTHONPATH=. poetry run pydoc-markdown`)

    console.log(`Snapshotting version...`)
    proc.execSync(`cd ${REPO_DOCS_DIR} && npm run docusaurus docs:version ${version}`)

    console.log(`Moving snapshot`)
    fs.cpSync(REPO_DOCS_DIR+"/"+VERSIONED_DOCS_FOLDER, VERSIONED_DOCS_FOLDER, {recursive: true})
    fs.cpSync(REPO_DOCS_DIR+"/"+VERSIONED_SIDEBARS_FOLDER, VERSIONED_SIDEBARS_FOLDER, {recursive: true})   
 
}

fs.cpSync(REPO_DOCS_DIR+"/versions.json", "versions.json")
