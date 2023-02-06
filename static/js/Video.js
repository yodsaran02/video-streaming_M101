if (screen.width < 420)
{
  video.style.height = "500px";
}
function playvideo(subject){
  var video = document.getElementById('video');
  var video_name = document.getElementById("date").value;
  var str = "http://"+ "jwind.tv" + ":3001/Video/"+subject+"/" + video_name;
  console.log(str);
  video.setAttribute("src", str);
  video.load();
  video.play();
}