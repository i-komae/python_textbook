#!/bin/sh

pdf_path="$1"

if [ -z "$pdf_path" ]; then
  exit 1
fi

for skim_app in "/Applications/Skim.app" "$HOME/Applications/Skim.app"; do
  if [ -d "$skim_app" ] && open -a "$skim_app" "$pdf_path"; then
    exit 0
  fi
done

if ! open "$pdf_path"; then
  printf '%s\n' "warning: no available application could open $pdf_path" >&2
fi

exit 0
