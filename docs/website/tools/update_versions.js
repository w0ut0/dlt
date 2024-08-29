const proc = require('child_process')

// TODO: get tags automatically, put newest version on top
VERSIONS = [
    "0.5.4",
    "0.4.12",
    "0.3.25"
]

let currentBranch = proc.execSync('git rev-parse --abbrev-ref HEAD').toString().trim()

console.log(`Currently on rev ${currentBranch}`)


for (const version of VERSIONS) {
    console.log(`Generating version ${version}`)
}

// back to current revision
proc.execSync(`git checkout ${currentBranch}`)

