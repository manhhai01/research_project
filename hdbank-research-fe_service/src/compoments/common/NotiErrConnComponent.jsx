import React from 'react'
import PageError from '../../assets/images/noti-err.jpg'
import { Button } from 'antd'

const NotiErrConnComponent = (props) => {
    return (
        <div className="text-center mt-5">
            <img src={PageError} alt="PageError" width={"85px"} />
            <p className='mt-3'><Button color="default" variant="text">
                {props.desc}
            </Button></p>
        </div>
    )
}

export default NotiErrConnComponent