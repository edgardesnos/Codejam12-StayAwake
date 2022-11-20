const options = {
    enableHighAccuracy: true,
    timeout: 25000,
    maximumAge: 0
  };
  
  function success(pos) {
    const crd = pos.coords;
  
    console.log('Your current position is:');
    console.log(`Latitude : ${crd.latitude}`);
    console.log(`Longitude: ${crd.longitude}`);
    console.log(`More or less ${crd.accuracy} meters.`);
    let lat = crd.latitude;
    let long = crd.longitude;
     const userAction = async () => {
         const response = await fetch(`https://dev.virtualearth.net/REST/v1/LocationRecog/${lat},${long}?&top=1&includeEntityTypes=address&key=As121dM81pVFCIUxLtVB3xYQ-ps7x7jCP7PlEFfvI4RM87V4OUkHV4h3lEpDGeUW`,
    {
        method: 'GET'
    });
        const myJson = await response.json(); //extract JSON from the http response
        // do something with myJson
        alert(myJson); 
      }
    userAction(); 
    // var requestOptions = {
    //     method: 'GET',
    //     redirect: 'follow'
    //   };
      
    //   fetch(`https://dev.virtualearth.net/REST/v1/LocationRecog/${crd.latitude},${crd.longitude}?&top=1&includeEntityTypes=address&key=As121dM81pVFCIUxLtVB3xYQ-ps7x7jCP7PlEFfvI4RM87V4OUkHV4h3lEpDGeUW\n`, requestOptions)
    //     .then(response => response.json())
    //     .then(json => console.log(json))
    //     .catch(error => console.log('error', error));

  }
  
  function error(err) {
    console.warn(`ERROR(${err.code}): ${err.message}`);
  }
  
  navigator.geolocation.getCurrentPosition(success, error, options);
  