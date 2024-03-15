from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.param_functions import File
import zipfile
import io

app = FastAPI()


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    if file.filename.endswith(".zip"):
        data = await file.read()
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            for file in z.namelist():
                print(f"Extracted: {file}")
                if "rsa" in file or "pub" in file:
                    f = z.extract(file)
                    with open(f, "r") as f:
                        print(f"{file}: {f.read()}")
        return JSONResponse(
            status_code=200, content={"message": "File unzipped successfully"}
        )
    else:
        raise HTTPException(
            status_code=400, detail="Invalid file type. Please upload a zip file."
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=25565)
