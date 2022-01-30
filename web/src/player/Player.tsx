import { useCallback, useEffect, useState } from "react"
import axios from "axios"
import axiosRetry from "axios-retry"

import WebPlayer from "./WebPlayer"
import Login from "./Login"

axiosRetry(axios, { retries: 5, retryDelay: axiosRetry.exponentialDelay })

export default function Player(): JSX.Element {
    const [token, setToken] = useState<string>()
    const [error, setError] = useState<string>()
    const [requestComplete, setRequestComplete] = useState<boolean>(false)

    const onReload = useCallback(() => {
        window.location.reload()
    }, [])

    useEffect(() => {
        async function getToken() {
            try {
                const resp = await axios.get(process.env.REACT_APP_API_URL + "/auth/token")
                if (resp.data.error) {
                    setError(resp.data.error)
                } else if (resp.data.token) {
                    setToken(resp.data.token)
                }
            } catch (error) {
                setError((error as Error).message)
            } finally {
                setRequestComplete(true)
            }
        }
        getToken()
    }, [])

    if (error) {
        return (
            <div>
                <p>Unable to load Player: {error}</p>
                <p><button onClick={onReload}>Reload Page</button></p>
            </div>
        )
    }

    if (!requestComplete) {
        return <div>Loading...</div>
    }

    if (!token) {
        return <Login />
    }

    return <WebPlayer token={token} />
}
