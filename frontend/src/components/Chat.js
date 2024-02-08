import React, { useState, useEffect } from "react";
import { Grid, Paper, Typography, List, ListItem, ListItemText, Divider } from '@material-ui/core';
import ChatIcon from '@material-ui/icons/Chat';
import Fab from '@material-ui/core/Fab';
import SendIcon from '@material-ui/icons/Send';
import TextField from '@material-ui/core/TextField';
/*
<Grid item xs={8}>
                <Paper style={{ padding: '20px', height: '100%', overflowY: 'auto' }}>
                    <Typography variant="h5" gutterBottom>
                        News Feed
                    </Typography>
                    <List>
                        {newsFeedData.map((item) => (
                            <div key={item.id}>
                                <ListItem>
                                    <ListItemText
                                        primary={item.title}
                                        secondary={item.content}
                                    />
                                </ListItem>
                                <Divider />
                            </div>
                        ))}
                    </List>
                </Paper>
            </Grid>*/

const newsFeedData = [
    {
        id: 1,
        title: 'Lorem Ipsum Dolor',
        content: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
        timestamp: new Date('2024-02-05T08:30:00'),
    },
    {
        id: 2,
        title: 'Consectetur Adipiscing',
        content: 'Consectetur adipiscing elit. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',
        timestamp: new Date('2024-02-05T12:45:00'),
    },
    {
        id: 3,
        title: 'Sed Do Eiusmod Tempor',
        content: 'Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.',
        timestamp: new Date('2024-02-06T09:15:00'),
    },
];

export default function Chat() {
    const [message, setMessage] = useState('');
    const [chatMessages, setChatMessages] = useState([]);
    const [ws, setWs] = useState(null);

    useEffect(() => {
        const socket = new WebSocket("ws://localhost:8080/ws/playlist/");

        setWs(socket);

        console.log("connecting");

        socket.onopen = () => {
            console.log("Successfully Connected");
        };

        socket.onmessage = (event) => {
            console.log(event.data);
            const receivedMessage = JSON.parse(event.data);
            setChatMessages((prevMessages) => [...prevMessages, receivedMessage]);
        };

        socket.onclose = (event) => {
            console.log("Socket Closed Connection: ", event);
        };

        socket.onerror = (error) => {
            console.log("Socket Error: ", error);
        };

        return () => {
            if (socket) {
                socket.close();
            }
        };

    }, []);

    const sendMessage = () => {
        if (message.trim() !== '' && ws && ws.readyState === WebSocket.OPEN) {
            const msgObj = { id: chatMessages.length + 1, sender: 'User2', msg: message };
            ws.send(JSON.stringify(msgObj));
            setMessage('');
        }
    };

    return (
        <Grid item xs="auto">
            <Paper style={{ padding: '20px', height: '100%', overflowY: 'auto' }}>
                <Typography variant="h5" gutterBottom>
                    Chat
                    <ChatIcon style={{ marginLeft: '10px' }} />
                </Typography>
                <List>
                    {chatMessages.map((msg) => (
                        <div key={msg.id}>
                            <ListItem>
                                <ListItemText
                                    primary={msg.sender}
                                    secondary={msg.msg}
                                />
                            </ListItem>
                            <Divider />
                        </div>
                    ))}
                </List>
                <Grid item xs="auto">
                    <TextField
                        id="standard-basic"
                        label="Enter..."
                        variant="standard"
                        value={message}
                        onChange={(e) => setMessage(e.target.value)} />
                    <Fab color="primary" aria-label="add" onClick={sendMessage}>
                        <SendIcon />
                    </Fab>
                </Grid>
            </Paper>
        </Grid>
    );
}
