import React from "react"

import { Device } from "./types"

interface PlaybackProps {
    deviceId: string
    currentDevice?: Device
    onTransfer: (_: React.MouseEvent<HTMLButtonElement>) => Promise<void>
}

export default function Playback(props: PlaybackProps): JSX.Element {
    if (props.currentDevice?.id === props.deviceId) {
        return <></>
    }

    return (
        <div>
            {props.currentDevice &&
                <>
                    <p>Currently Playing on</p>
                    <p>{props.currentDevice.name}</p>
                </>
            }
            <div>
                <button onClick={props.onTransfer}>Transfer Playback Here</button>
            </div>
        </div>
    )
}
