import React from 'react'

import Player from "./player/Player";

import './App.css'


export default function App(): JSX.Element {
    return (
        <div className="App">
            <header className="App-header">
                <Player />
            </header>
        </div>
    )
}
