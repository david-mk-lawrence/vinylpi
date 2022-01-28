import React, { useState, useCallback } from "react"
import axios from "axios"

export default function Reader(): JSX.Element {
    const [isReading, setIsReading] = useState<boolean>(false)
    const [isWriting, setIsWriting] = useState<boolean>(false)
    const [error, setError] = useState<Error>()
    const [uri, setUri] = useState<string>()

    const onRead = useCallback(async (_: React.MouseEvent<HTMLButtonElement>) => {
        setIsReading(true)
        try {
            await axios.put(process.env.REACT_APP_API_URL + "/reader/read")
        } catch (error: unknown) {
            setError(error as Error)
        } finally {
            setIsReading(false)
        }
    }, [])

    const onWrite = useCallback(async (_: React.MouseEvent<HTMLButtonElement>) => {
        setIsWriting(true)
        try {
            await axios.put(process.env.REACT_APP_API_URL + "/reader/write", {"uri": uri})
        } catch (error: unknown) {
            setError(error as Error)
        } finally {
            setIsWriting(false)
        }
    }, [uri])

    const onUriChange = useCallback(async (event: React.ChangeEvent<HTMLInputElement>) => {
        setUri(event.currentTarget.value)
    }, [])

    if (error) {
        return <p>Error: {error}</p>
    }

    if (isReading) {
        return <p>Waiting to read card...</p>
    }

    if (isWriting) {
        return <p>Waiting to write card...</p>
    }

    return (
        <div>
            <div>
                <button onClick={onRead}>Read</button>
            </div>
            <div>
                <input type="text" onChange={onUriChange} />
                <button onClick={onWrite}>Write</button>
            </div>
        </div>
    )
}
