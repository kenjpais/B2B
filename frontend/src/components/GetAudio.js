import { Grid, Typography, ListItem, ListItemText } from '@material-ui/core';
import React, { useEffect, useRef, useState } from 'react';

const GetAudio = () => {
    const audioRef = useRef();
    const [filenames, setFileNames] = useState([]);
    const [filename, setFileName] = useState('');
    //var filename = "nothing";

    useEffect(() => {
        const fetchAudioStream = async () => {
            try {
                const response = await fetch('http://localhost:8000/api/get-audio');
                const blob = await response.blob();
                const audioUrl = URL.createObjectURL(blob);

                const res = await fetch('http://localhost:8000/api/get-filenames/');
                if (!res.ok) {
                    throw new Error('Network response not ok');
                }
                const data = await res.json();
                console.log("response:", data);

                console.log(data[0]);
                setFileName(data[0]);
                setFileNames(data);
                // Play the audio
                audioRef.current.src = audioUrl;
                audioRef.current.play();
            } catch (error) {
                console.error('Error fetching audio:', error);
            }
        };
        fetchAudioStream();
    }, []);

    return (
        <Grid container spacing={2} alignItems='auto'>
            <Grid item xs={12}>
                {filenames.map((item, index) => (
                    <ListItem key={index}>
                        <ListItemText primary={item} />
                    </ListItem>
                ))}
            </Grid>
            <Grid item xs={12}>
                <Typography>{filename}</Typography>
            </Grid>
            <Grid item xs={12}>
                <audio ref={audioRef} controls />
            </Grid>

        </Grid>
    );
};

export default GetAudio;
