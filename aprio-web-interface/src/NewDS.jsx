import { useState, useRef, useEffect } from "react";
import UploadLogo from "./images/UploadLogo";
import axios from "axios";
import { api } from "./env";

const NewDS = () => {

    const [stage, setStage] = useState("upload")
    const [file, setFile] = useState(null)
    const fileInputRef = useRef(null);
    const [error, setError] = useState(null)

    const handleFileChange = (event) => {
        // Update the state with the selected file
        setFile(event.target.files[0]);
      };
    
      const handleImageClick = () => {
        // Trigger the file input click when the image is clicked
        fileInputRef.current.click();
      };
      const accepted_formats = ['csv', 'xlsx']
      useEffect(()=>{
        if (file){
            if(accepted_formats.includes(file.name.split('.')[1])){
                setStage('submit')
            }else{
                setError("please upload a csv or an xlsx file")
                setTimeout(()=> {
                    setError(null)
                }, 3000)
            }
        }
      }, [file])

      const upload_file_to_server = async ()  => {
        const formData = new FormData();
  formData.append('file', file);
  try {
      console.log('uploading file')
      console.log(formData['file'])
    const response = await axios.post(api+'NewDS', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    console.log('File uploaded successfully:', response.data);
  } catch (error) {
    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      console.error('Server responded with an error:', error.response.data);
      console.error('Status code:', error.response.status);
      console.error('Headers:', error.response.headers);
    } else if (error.request) {
      // The request was made but no response was received
      console.error('No response received from the server');
    } else {
      // Something happened in setting up the request that triggered an Error
      console.error('Error during request setup:', error.message);
    }

    console.error('Axios error config:', error.config);
  }

      }

    return ( 
        <div className="newDsPage" >

            {error && 
                <div className="error-container">
                    {error}
                </div>
            }

            {!error && stage == "upload" && 
                <div onClick={handleImageClick} className="upload-container" >

                    <UploadLogo />
                    <input
                        type="file"
                        ref={fileInputRef}
                        style={{ display: 'none' }}
                        onChange={handleFileChange}
                    />
                    <h2>Upload File</h2>
                </div>
            }
            {
                !error && stage === "submit" &&
                <div className="submit-container">
                    <div className="info">
                        <div> Filename: <b>{file.name}</b></div>
                        <div>File Size: <b>{(file.size / (1024 * 1024)).toFixed(4)} mb</b></div>
                    </div>
                    <div className="submit">
                        <button className="submit-btn" onClick={upload_file_to_server} >
                            Submit File
                        </button>
                    </div>
                </div>
            }
        </div>
     );
}
 
export default NewDS;