import React from "react"

export default function Login(): JSX.Element {
    return <a href={process.env.REACT_APP_BACKEND_URL + "/auth/login"}>Login</a>
}
