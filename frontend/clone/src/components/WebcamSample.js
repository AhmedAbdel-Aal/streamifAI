// import React, { useRef, useState } from 'react';
// import Webcam from 'react-webcam';

// function WebcamSample() {

//     const [isShowVideo, setIsShowVideo] = useState(false);
//     const videoElement = useRef(null);
    
//     const videoConstraints = {
//         width: 640,
//         height: 480,
//         facingMode: "user"
//     }

//     const startCam = () => {
//         setIsShowVideo(true);
//     }

//     const stopCam = () => {
//         let stream = videoElement.current.stream;
//         const tracks = stream.getTracks();
//         tracks.forEach(track => track.stop());
//         setIsShowVideo(false);
//     }

//     return (
//         <div class='centerScreen'>
//             <div className="camView"  class='centerScreen'>
//                 {isShowVideo &&
//                     <Webcam audio={false} ref={videoElement} videoConstraints={videoConstraints} />
//                 }
//             </div>
//             <button onClick={startCam}>Start Camera</button>
//             <button onClick={stopCam}>Close Camera</button>
//         </div>
//     );
// };

// export default WebcamSample;