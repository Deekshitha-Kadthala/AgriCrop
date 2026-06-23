import os
import uuid
import shutil


def save_uploaded_image(file, upload_folder):

    os.makedirs(
        upload_folder,
        exist_ok=True
    )

    extension = file.filename.split(".")[-1]

    filename = f"{uuid.uuid4()}.{extension}"

    filepath = os.path.join(
        upload_folder,
        filename
    )

    with open(filepath, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    return filename, filepath