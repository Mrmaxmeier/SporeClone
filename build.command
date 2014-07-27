cd "$(dirname "$0")"
echo "Removing Build Folder"
rm -Rf build
echo "Building BUNDLE & DISK IMAGE"
python3 build.py bdist_mac --iconfile icon.icns bdist_dmg
