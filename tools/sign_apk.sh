#!/bin/bash
# usage: sign_apk.sh <apk> <abi>
# Signs with a throwaway key made for this build, then checks the result.
set -euo pipefail
APK="$1"
ABI="$2"
SDK="${ANDROID_HOME:-${ANDROID_SDK_ROOT:?Android SDK not found}}"
TOOLS="$(ls -d "${SDK}"/build-tools/* | sort -V | tail -1)"
KEY="${RUNNER_TEMP}/sign.keystore"
if [[ ! -f "${KEY}" ]]; then
  openssl rand -hex 16 > "${KEY}.pass"
  keytool -genkeypair -keystore "${KEY}" -storepass "$(cat "${KEY}.pass")" -keypass "$(cat "${KEY}.pass")" \
    -alias app -keyalg RSA -keysize 2048 -validity 10000 -dname "CN=Personal Build"
fi
"${TOOLS}/apksigner" sign --ks "${KEY}" --ks-pass "file:${KEY}.pass" --ks-key-alias app "${APK}"
"${TOOLS}/apksigner" verify --verbose "${APK}"
"${TOOLS}/zipalign" -c 4 "${APK}"
"${TOOLS}/aapt" dump xmltree "${APK}" AndroidManifest.xml > "${RUNNER_TEMP}/manifest.txt"
for P in INTERNET ACCESS_NETWORK_STATE ACCESS_WIFI_STATE; do
  grep -q "\"android.permission.${P}\"" "${RUNNER_TEMP}/manifest.txt" || { echo "Missing permission ${P}"; exit 1; }
done
unzip -l "${APK}" > "${RUNNER_TEMP}/files.txt"
grep -q "lib/${ABI}/libgodot_android.so" "${RUNNER_TEMP}/files.txt" || { echo "No ${ABI} engine inside the APK"; exit 1; }
grep "lib/" "${RUNNER_TEMP}/files.txt"
unzip -tq "${APK}"
