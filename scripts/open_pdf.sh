#!/bin/sh

pdf_path="$1"

if [ -z "$pdf_path" ]; then
  exit 1
fi

if [ -d "/Applications/Skim.app" ] || [ -d "$HOME/Applications/Skim.app" ]; then
  open -a Skim "$pdf_path"
else
  open "$pdf_path"
fi
