dizin_yolu="$1"
kabuk_yolu="$2"

if [[ ":$PATH:" == *":$dizin_yolu:"* ]]; then
	echo "ZATEN PATH'E EKLENMIS"
else
  echo "export PATH=\"\$PATH:$dizin_yolu\"" >> $kabuk_yolu
	source $kabuk_yolu
	echo "DIZIN PATH SONUNA EKLENDI"
fi
