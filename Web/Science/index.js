// Create event listener for all link clicks
document.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', (e) => {
    // Retrieve href and store in targetUrl variable
    let targetUrl = e.target.href;
    // Output value of targetUrl to console
    console.log('A link with target URL ' + targetUrl + 'was clicked');
		var video = document.getElementById('video');
		var str = targetUrl.replace("/Web/Science/Science.html#",":3000/Video/Science/");
	   video.setAttribute("src", str);
		video.load();
		video.play();
	 
  });
});
