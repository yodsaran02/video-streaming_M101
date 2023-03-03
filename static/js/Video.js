if (screen.width < 420)
{
  video.style.height = "500px";
}
function playvideo(subject){
  var video = document.getElementById('video');
  var video_name = document.getElementById("date").value;
  var str = "http://"+ "jwind.tv" + ":3001/Video/"+subject+"/" + video_name;
  video.setAttribute("src", str);
  video.load();
  video.play();
}

function copylink(subject){
  var video_name = document.getElementById("date").value;
  var button = document.getElementById("copylink")
  var video_link = "http://jwind.tv/video?subject="+subject+"&date="+ video_name;
  console.log(video_link)
  navigator.clipboard.writeText(video_link);
  button.innerHTML = "Copied!";
  const texttimeout = setTimeout(function (){button.innerHTML = "Copylink";},2000); 
}
function copylinks(){
  var button = document.getElementById("copylink")
  navigator.clipboard.writeText(window.location.href);
  button.innerHTML = "Copied!";
  const texttimeout = setTimeout(function (){button.innerHTML = "Copylink";},2000); 
}