#!/bin/sh

[ -z $HOST ] && HOST='http://root.cypherd.org'
[ -z $EDITOR ] && EDITOR='vim'

FILE=$1
if [[ -z $FILE ]]; then
  FILE=`mktemp /tmp/cypherd.XXXXXXXXX`
  $EDITOR $FILE
  DELETE_AFTER=1
else
  DELETE_AFTER=0
fi

echo "Sign document?"
select yn in "Yes" "No"; do
  if [[ "$yn" == "Yes" ]]; then
    INPUT_FILE=$FILE
    FILE=`mktemp /tmp/cypherd.XXXXXXXXX`

    # Remove file to prevent gpg from complaining about overwriting the output file
    rm $FILE
    gpg -o $FILE --clearsign $INPUT_FILE

    DELETE_AFTER=1
  fi
  break
done

if $(which md5sum); then
  MD5=md5sum
else
  MD5='md5 -q'
fi

MD5SUM=`$MD5 $FILE`

echo 'Getting upload URL...'
UPLOAD_URL=`curl -s $HOST/url`

echo 'Uploading...'
curl -X POST -F md5sum=$MD5SUM -F document=@$FILE $UPLOAD_URL

if [[ $DELETE_AFTER -ne 0 ]]; then
  rm $FILE
fi
