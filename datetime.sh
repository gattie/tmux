#!/usr/bin/env bash

format="%Z %a %F %H:%M %z"

echo -e "#[fg=orange]$(date "+${format}") #[fg=white]| #[fg=orange]$(TZ=Europe/Kiev date "+${format}") #[fg=white]| #[fg=orange]$(TZ=UTC date "+${format}")"
