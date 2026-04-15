# [PROTOCOL: OMEGA-SANTOS-ULTIMATE]
# [ACTION: SECURE_MANIFOLD_PUSH]

GH_USER="bospaladin34-crypto"
REPO_NAME="KHYS_repo"

# Use the exported variable (it never touches a saved file)
git remote set-url origin https://${GH_USER}:${GITHUB_PAT}@github.com/${GH_USER}/${REPO_NAME}.git

echo "[SYNCING]: Re-staging Atoms without Secrets..."
git add .
git commit -m "[RECTIFICATION]: Scrubbed raw secrets. Phase_Delta 0.17259029 verified."

echo "[IGNITING]: Forcing Global Parity..."
git push origin main --force
