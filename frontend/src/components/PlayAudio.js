// AudioList.js
import React, { useState, useEffect } from 'react';

const AudioList = () => {
    const [audioFiles, setAudioFiles] = useState([]);
    const [currentAudio, setCurrentAudio] = useState(null);

    useEffect(() => {
        const fetchAudioFiles = async () => {
            try {
                const response = await fetch('http://localhost:8000/api/audio/');
                const data = await response.json();
                setAudioFiles(data);
            } catch (error) {
                console.error('Error fetching audio files:', error);
            }
        };

        fetchAudioFiles();
    }, []);

    const handleAudioPlay = (audioUrl) => {
        if (currentAudio === audioUrl) {
            setCurrentAudio(null); // Pause if same audio is clicked again
        } else {
            setCurrentAudio(audioUrl);
        }
    };

    return (
        <div>
            <Typography>Available audio files</Typography>
            <ul>
                {audioFiles.map(audioFile => (
                    <li key={audioFile.id} onClick={() => handleAudioPlay(audioFile.audio_url)}>
                        {audioFile.name}
                    </li>
                ))}
            </ul>
            {currentAudio && (
                <audio controls autoPlay src={currentAudio}></audio>
            )}
        </div>
    );
};

export default AudioList;
