// // var url = window.location.href;

// // let res=true

// //     fetch( 'http://localhost:5000/post?URL=${url}' )
// //     .then( response => response.text() )
// //     .then( response => {
// //         // Do something with response.
// //         //res=response
// //         console.log(response)
        
// //         if(response==1){
// // 		document.getElementById("myElement").innerText = "Suspicious";
// //         }
// //         else if(response==0){
// // 		document.getElementById("myElement").innerText = "Safe Website"
// //         }
// //         else if(response==-1){
// // 		document.getElementById("myElement").innerText = "Phishing"
// //         }
// //     } );

// const url = window.location.href;
// const element = document.getElementById("site_score");
// const element_2 = document.getElementById("site_msg");
// // responseText.innerText="Results will appear here"
// fetch('http://localhost:5000/post', {
//   method: 'POST',
//   headers: {
//     'Content-Type': 'application/x-www-form-urlencoded'
//   },
//   body: `URL=${url}`
// })
// .then(response => response.text())
// .then(data => {
// 	console.log('Server response:', data);
//   if (data === '1') {
// 	  document.getElementById("site_score").innerText = 'Suspicious'
// 	  document.getElementById("site_msg").innerText = 'This website may not be safe >_<'
// 	  document.getElementById("site_score").style.background = "linear-gradient(45deg, #a64812, #e1e354);";
// 	document.getElementById("site_score").style.transform = "translateZ(25px)";
//   } else if (data === '0') {
// 	document.getElementById("site_score").innerText = 'Safe'
// 	document.getElementById("site_msg").innerText = 'This website is safe to use UwU'
// 	document.getElementById("site_score").style.background = "linear-gradient(45deg, #00db2f, #06678b)";
// 	document.getElementById("site_score").style.transform = "translateZ(25px)";
//   } else if (data === '-1') {
// 	document.getElementById("site_score").innerText = 'Phishing'
// 	document.getElementById("site_msg").innerText = 'This website is not safe to use T_T'
// 	document.getElementById("site_score").style.background = "linear-gradient(45deg, #900000, #6d6f08);";
// 	document.getElementById("site_score").style.transform = "translateZ(25px)";
// 	}

// })
// .catch(error => console.error(error));



// document.addEventListener('DOMContentLoaded', function() {
// 	const url = window.location.href;
// 	const element = document.getElementById("site_score");
// 	const element_2 = document.getElementById("site_msg");
// 	// onClick's logic below:
// 	link.addEventListener('click', function() {
// 	    hellYeah('xxx');
// 	});
//     });


// document.addEventListener("DOMContentLoaded", function() {
// var background = chrome.extension.getBackgroundPage();
// const url = window.location.href;


// ----------------------------------------------------
chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
	var tab = tabs[0];
	var url = tab.url;

	const el = document.getElementById("site_score");
	const el2 = document.getElementById("site_msg");
	const icon = document.getElementById("status-icon"); // ✅ Icon element reference added

	fetch('http://localhost:5000/post', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/x-www-form-urlencoded'
		},
		body: `URL=${url}`
	})
	.then(response => response.text())
	.then(data => {
		console.log('Server response:', data);

		if (parseInt(data) == 1 ) {
			alert('Suspicious');
			console.log('1');
			el.textContent = 'Suspicious';
			el2.textContent = "⚠️ This website may be suspicious. Proceed with caution.";
			el.style.background = "linear-gradient(45deg, #a64812, #e1e354)";
			el.style.transform = "translateZ(25px)";
			icon.src = "icons/suspicious-icon.png"; // ✅ set suspicious icon
			icon.alt = "Suspicious";
			
		} else if (parseInt(data) == 0 ) {
			console.log('0');
			el.textContent = 'Safe';
			el2.textContent = "✅ This website appears safe to use.";
			el.style.background = "linear-gradient(45deg, #00db2f, #06678b)";
			el.style.transform = "translateZ(25px)";
			icon.src = "icons/safe-icon.png"; // ✅ set safe icon
			icon.alt = "Safe";

		} else if (parseInt(data) == -1 ) {
			alert('Phising');
			console.log('-1');
			el.textContent = 'Phishing';
			el2.textContent = "🚨 Phishing site detected! Do NOT enter sensitive info.";
			el.style.background = "linear-gradient(45deg, #900000, #6d6f08)";
			el.style.transform = "translateZ(25px)";
			icon.src = "icons/phishing-icon.png"; // ✅ set phishing icon
			icon.alt = "Phishing";
		}
	})
	.catch(error => {
		console.error('Fetch error:', error);
		if (icon) {
			icon.src = "icons/error-icon.png"; // ✅ set error icon
			icon.alt = "Error";
		}
	});
});

//mail - sms spamm
function checkSpamMessage(text) {
  fetch('http://localhost:5000/predict_spam', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: `message=${encodeURIComponent(text)}`
  })
  .then(res => res.text())
  .then(data => {
    if (data === "spam") {
      alert("⚠️ This message looks like SPAM.");
    } else {
      alert("✅ This message appears safe.");
    }
  })
  .catch(err => {
    alert("Server error.");
    console.error(err);
  });
}


// });




// document.addEventListener("DOMContentLoaded", function () {
	// const url = window.location.href;
	// const el = document.getElementById("site_score");
	// const el2 = document.getElementById("site_msg");
	// // responseText.innerText="Results will appear here"
	// fetch("http://localhost:5000/post", {
	//   method: "POST",
	//   headers: {
	//     "Content-Type": "application/x-www-form-urlencoded",
	//   },
	//   body: `URL=${url}`,
	// })
	//   .then((response) => response.text())
	//   .then((data) => {
	//     console.log("Server response:", data);
	//     if (data === "1") {
	//       console.log("Suspicious");
	//       el.textContent = "Suspicious";
	//       el2.textContent = "This website may not be safe >_<";
	//       el.style.background = "linear-gradient(45deg, #a64812, #e1e354);";
	//       el.style.transform = "translateZ(25px)";
	//     } else if (data === "0") {
	//       console.log("Safe");
	//       el.textContent = "Safe";
	//       el2.textContent = "This website is safe to use UwU";
	//       el.style.background = "linear-gradient(45deg, #00db2f, #06678b)";
	//       el.style.transform = "translateZ(25px)";
	//     } else if (data === "-1") {
	//       console.log("Phishing");
	//       el.textContent = "Phishing";
	//       el2.textContent = "This website is not safe to use T_T";
	//       el.style.background = "linear-gradient(45deg, #900000, #6d6f08);";
	//       el.style.transform = "translateZ(25px)";
	//     } else {
	//       console.log("Unknown response from server:", data);
	//     }
	//   })
	//   .catch((error) => {
	//     console.error("Fetch error:", error);
	//   });
//       });
      



// const url = window.location.href;
// // responseText.innerText="Results will appear here"
// fetch('http://localhost:5000/post', {
//   method: 'POST',
//   headers: {
//     'Content-Type': 'application/x-www-form-urlencoded'
//   },
//   body: `URL=${url}`
// })
// .then(response => response.text())
// .then(data => {
//   console.log('Server response:', data);
//   if (data === '1' ) {
// 	alert('Suspicious');
// 	console.log('Suspicious');
	
//   } else if (data === '0' ) {
// 	alert('Safe');
// 	console.log('Safe');
	
//   } else if (data === '-1' ) {
// 	alert('Phising');
// 	console.log('Phishing');
//   }
// })
// .catch(error => {
//   console.error('Fetch error:', error);
// });