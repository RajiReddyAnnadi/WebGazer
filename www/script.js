// webgazer.setGazeListener(function(data, elapsedTime) {
//     if (data == null) {
//         return;
//     }
//     var xprediction = data.x; //these x coordinates are relative to the viewport
//     var yprediction = data.y; //these y coordinates are relative to the viewport
//     console.log(elapsedTime); //elapsed time is based on time since begin was called
//     console.log(data.x);
//     console.log(data.y);
// }).begin();
if(!window.scriptLoadFlag){
    window.scriptLoadFlag = true
    var globalVariable = {};
    var predictionList = []
    var chunks = [];
}
function startVideoandScreenRecording(){
    console.log("startVideoandScreenRecording")
    navigator.mediaDevices.getUserMedia({
        video:  {
            facingMode: 'user', mirrored: true 
        },
        audio: true
    }).then(async function(stream) {
        let recorder = RecordRTC(stream, {
            type: 'video'
        });
        recorder.startRecording();
        recorder.camera = stream;
        globalVariable.videoRecorder = recorder;
    });
    navigator.mediaDevices.getDisplayMedia({
    video: {
        mediaSource: 'screen',
        // displaySurface: 'window', // monitor, window, application, browser
        logicalSurface: true,
        cursor: 'never' // never, always, motion
    }, 
    audio: true
    }).then(async function(stream) {
    // let recorder = RecordRTC(stream, {
    //     type: 'video'
    // });
    // recorder.startRecording();
    // recorder.screen = stream;
    // globalVariable.screenRecorder = recorder;
    var options = {mimeType: 'video/webm; codecs=vp9'};
    var mediaRecorder = new MediaRecorder(stream, options);
    globalVariable.mediaRecorder = mediaRecorder;
    globalVariable.screen = stream;
    mediaRecorder.start();
    mediaRecorder.ondataavailable = function(e) {
        chunks.push(e.data);
    }
    mediaRecorder.onstop = function(e) {
        var blob = new Blob(chunks, { 'type' : 'video/webm; codecs=vp9'});
        // invokeSaveAsDialog(blob, "ScreenRecording"+Date.now()+".webm");
        var url = URL.createObjectURL(blob);
        var a = document.createElement('a');
        document.body.appendChild(a);
        a.style = 'display: none';
        a.href = url;
        a.download = "ScreenRecording"+Date.now()+".webm";
        a.click();
        window.URL.revokeObjectURL(url);
    }
    });
}


function stopRecording(){
    //stopping video recording
    console.log("stopRecording")
    // return false;
    let videoRecorder =  globalVariable.videoRecorder;
    console.log("stopRecording2")
    videoRecorder.stopRecording(function() {
        let blob = videoRecorder.getBlob();
        invokeSaveAsDialog(blob, "VideoRecording"+Date.now()+".webm");
    });
    videoRecorder.camera.stop();
    console.log("stopRecording3")
    let mediaRecorder =  globalVariable.mediaRecorder;
    mediaRecorder.stop();
    globalVariable.screen.stop();
    $("#preTestPage").hide()
    $("#endpage").show();
    console.log(predictionList)
    download("GazePredictions.txt", predictionList)
    return false;
}

function download(filename, text) {
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', filename);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

function callGazeListener(){
    console.log("callGazeListener")
    console.log(window.flag)
    webgazer.setGazeListener(function(data, elapsedTime) {
        if (data == null) {
            return;
        }
        // var xprediction = data.x; //these x coordinates are relative to the viewport
        // var yprediction = data.y; //these y coordinates are relative to the viewport
        // console.log(elapsedTime); //elapsed time is based on time since begin was called
        // console.log(data.x);
        // console.log(data.y);
        var item = [data.x, data.y, elapsedTime]
        predictionList.push(item);
    }).begin();
}

function myscript(){
    var PointCalibrate = 0;
    var CalibrationPoints={};
    console.log("webgazer in .js")
    console.log(webgazer)
    console.log($(".Calibration"))
    var flag = false
    
    $(".Calibration").click(function(){ // click event on the calibration buttons
        console.log("wefe")
        
        var id = $(this).attr('id');
        if (!CalibrationPoints[id]){ // initialises if not done
            CalibrationPoints[id]=0;
        }
        CalibrationPoints[id]++; // increments values
        if (CalibrationPoints[id]==5){ //only turn to yellow after 5 clicks
            $(this).css('background-color','yellow');
            $(this).prop('disabled', true); //disables the button
            PointCalibrate++;
            console.log(id)
            console.log(id.substring(2))
            var msg = new SpeechSynthesisUtterance(id.substring(2) + " completed");
        window.speechSynthesis.speak(msg);
        }else if (CalibrationPoints[id]<5){
            //Gradually increase the opacity of calibration points when click to give some indication to user.
            var opacity = 0.2*CalibrationPoints[id]+0.2;
            $(this).css('opacity',opacity);
        }
        
        //Show the middle calibration point after all other points have been clicked.
        if (PointCalibrate == 8){
            $("#Pt5").show();
        }

        if (PointCalibrate >= 9){ //revert to 9
            // await sleep(1500);
            $("#homepage").hide()
            $("#preTestPage").show()
        }
    })
}//myscripot closing brace
