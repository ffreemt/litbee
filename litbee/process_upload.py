"""Process uploads."""
# pylint: disable=invalid-name, unused-import
from typing import Union

from pathlib import Path
import tempfile
import cchardet
from logzero import logger


def process_upload(upload: Union[str, tempfile._TemporaryFileWrapper, bytes]) -> str:
    """Process upload (fileobj or bytes(zip file: io.BytesIO further to zipfile.ZipFile)).

    gr.inputs.File("file"): upload normal file
    gr.inputs.File("bytes"): upload zip file

    """
    # filename/path
    if isinstance(upload, str):
        fpath = Path(upload)
    elif isinstance(upload, bytes):
        logger.warning("Not implemented, yet, for zip file")
        return "Not implemented, yet, for zip file"
    else:
        try:
            fpath = Path(upload.name)
        except Exception as e:
            logger.error("Path(upload.name) error: %s", e)
            return str(e)

    suffixes = [
        "",
        ".txt",
        ".text",
        ".md",
        "tsv",
    ]
    # check .txt .md ''(no suffix)
    if fpath.suffix.lower() not in suffixes:
        logger.warning('suffix: [%s] not in %s', fpath.suffix, suffixes)
        # return "File type not supported, yet."

    try:
        # data = Path(upload.name).read_bytes()
        data = fpath.read_bytes()
    except Exception as e:
        logger.error("Unable to read data from %s, errors: %s", fpath, e)
        data = str(e).encode()

    # no data, empty file, return ""
    if not data:
        logger.info("empty file: %s", fpath)
        return ""

    encoding = cchardet.detect(data).get("encoding")

    if encoding is not None:
        try:
            text = fpath.read_text(encoding=encoding)
        except Exception as e:
            logger.error("Unable to retrieve text, error: %s", e)
            text = str(e)

        # return f"{upload.name} {type(upload)}\n\n{text}"
        # return f"{upload.name}\n{text}"
        return text

    # not able to cchardet: encoding is None, docx, pdf, epub, zip etc
    logger.info("Trying docx...to be implemented")

    # TODO .docx .epub .mobi .pdf etc.

    # _ = Path(upload.name)
    _ = Path(fpath)
    msg = f"binary file: {_.stem[:-8]}{_.suffix}"
    logger.warning("%s", msg)

    return msg


_ = '''  # colab gradio-file-inputs-upload.ipynb
# file_to_text/process_file
def zip_to_text(file_obj):
  """
  # zf = zipfile.ZipFile('german-recipes-dataset.zip')
  zf = file_obj
  namelist = zipfile.ZipFile.namelist(zf);
  # filename = zf.open(namelist[0]);
  file_contents = []
  for filename in namelist:
    with zf.open(filename) as fhandle:
      file_contents.append(fhandle.read().decode())
  """
  # fileobj is <class 'tempfile._TemporaryFileWrapper'>

  # gr.inputs.File("bytes")
  if isinstance(file_obj, bytes):
    data = file_obj.decode()
    return f"{type(file_obj)}\n{dir(file_obj)}\n{data}"

  # "file"/gr.inputs.File("file")  file_obj.name: /tmp/READMEzm8hc5ze.md
  data = Path(file_obj.name).read_bytes()
  return f"{file_obj.name} {type(file_obj)}\n{dir(file_obj)} \n{data}"
# '''
