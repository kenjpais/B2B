import React, { useEffect, useRef, useState } from 'react';
import { Grid, Typography, ListItem, ListItemText } from "@material-ui/core";

const AudioPlayer = () => {
    const audioRef = useRef();
    const [title, setTitle] = useState('');
    const [file, setFile] = useState(null);
    const [fileNames, setfileNames] = useState([]);
    var uploadedFiles = []
    /*
    useEffect(() => {
        try {
            const playTrack = async () => {
                const response = await fetch('http://localhost:8000/api/get-audio');
                const blob = await response.blob();
                const audioUrl = URL.createObjectURL(blob);
                audioRef.current.src = audioUrl;
                audioRef.current.play();
            }
        }
        catch (e) {
            console.log("failed to fetch audio");
        }

    }, []);
    */

    const playTrack = async () => {
        try {
            const response = await fetch('http://localhost:8000/api/get-audio');
            const blob = await response.blob();
            const audioUrl = URL.createObjectURL(blob);
            audioRef.current.src = audioUrl;
            audioRef.current.play();
        }
        catch (e) {
            console.log("failed to fetch audio");
        }
    };

    const handleTitleChange = (e) => {
        setTitle(e.target.value);
    };

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('name', title);
        formData.append('audio_file', file);
        try {
            const response = await fetch('http://localhost:8000/api/upload-audio', {
                method: 'POST',
                body: formData
            });
            if (response.ok) {
                alert('Music file uploaded successfully!');
                uploadedFiles.push(title);
                console.log(uploadedFiles);
                setfileNames(uploadedFiles);
            } else {
                throw new Error('Failed to upload music file');
            }
        } catch (error) {
            console.error('Error uploading music file:', error);
            alert('Error uploading music file. Please try again.');
        }
    };

    return (
        <Grid container spacing={12}>
            <Grid item xs={12}>
                {fileNames.map((item, index) => (
                    <ListItem key={index}>
                        <ListItemText primary={item} onClick={playTrack} />
                    </ListItem>
                ))}
            </Grid>
            <Grid item xs={12}>
                <div>
                    <h2>Upload Music</h2>
                    <form onSubmit={handleSubmit}>
                        <label>Title:</label>
                        <input type="text" value={title} onChange={handleTitleChange} required />
                        <label>File:</label>
                        <input type="file" onChange={handleFileChange} accept="audio/*" required />
                        <button type="submit">Upload</button>
                    </form>
                </div>
            </Grid>
            <Grid item xs={12}>
                <audio ref={audioRef} controls />
            </Grid>

        </Grid>
    );
};

export default AudioPlayer;