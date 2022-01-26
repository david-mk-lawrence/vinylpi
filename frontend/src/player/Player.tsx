import React, { useEffect, useState } from "react"
import axios from "axios"

import WebPlayer from "./WebPlayer"
import Login from "./Login"

interface LocalState {
    token?: string
    error?: string
    gotToken: boolean
}

export default function Player(): JSX.Element {
    const [localState, setLocalState] = useState<LocalState>({ token: undefined, error: undefined, gotToken: false })

    useEffect(() => {
        axios.get("/auth/token").then((resp) => {
            if (resp.data.error) {
                setLocalState({ token: undefined, error: resp.data.error, gotToken: true })
            } else if (resp.data.token) {
                setLocalState({ token: resp.data.token, error: undefined, gotToken: true })
            } else {
                setLocalState({ token: undefined, error: undefined, gotToken: true })
            }
        })
    }, [])

    if (!localState.gotToken) {
        return <div>Getting token...</div>
    }

    if (localState.error) {
        return (
            <div>
                <p>Error Getting Token: {localState.error}</p>
                <Login />
            </div>
        )
    }

    if (!localState.token) {
        return <Login />
    }

    return <WebPlayer token={localState.token} />
}
