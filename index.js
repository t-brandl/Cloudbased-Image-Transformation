let selected_mode = 0;
const apiUrl = 'http://localhost:2017';

  function getScaleMultiplier(){
    let radios = document.getElementsByName('scale');
    let scale_multiplier = 2;

    for (var i = 0, length = radios.length; i < length; i++)
    {
      if (radios[i].checked)
      {
        return scale_multiplier = radios[i].value;
      }
    }
  }

  function blackwhite(){
    selected_mode = 1;
	  document.getElementById("top").innerHTML = "Black and White Filter"; 
    document.getElementById("image_selection").style.display = "block";
    document.getElementById("scale_select").style.display = "none";
    document.getElementById("confirm").style.display = "block";
    document.getElementById("bw_example").style.display = "block";
    document.getElementById("us_example").style.display = "none";
    document.getElementById("cf_example").style.display = "none";
    document.getElementById("result").style.display = "none";
    document.getElementById("Failed").innerHTML = " ";
    document.getElementById("ItemPreview").src = " "; 
  }

  function upscale(){
    selected_mode = 2;
	  document.getElementById("top").innerHTML = "Upscale an Image"; 
    document.getElementById("image_selection").style.display = "block";
    document.getElementById("scale_select").style.display = "block";
    document.getElementById("confirm").style.display = "block";
    document.getElementById("bw_example").style.display = "none";
    document.getElementById("us_example").style.display = "block";
    document.getElementById("cf_example").style.display = "none";
    document.getElementById("result").style.display = "none";
    document.getElementById("Failed").innerHTML = " ";
    document.getElementById("ItemPreview").src = " "; 
  }

  function cartoonify(){
    selected_mode = 3;
	  document.getElementById("top").innerHTML = "Cartoonify an Image"; 
    document.getElementById("image_selection").style.display = "block";
    document.getElementById("scale_select").style.display = "none";
    document.getElementById("confirm").style.display = "block";
    document.getElementById("bw_example").style.display = "none";
    document.getElementById("us_example").style.display = "none";
    document.getElementById("cf_example").style.display = "block";
    document.getElementById("result").style.display = "none";
    document.getElementById("Failed").innerHTML = " ";
    document.getElementById("ItemPreview").src = " "; 
  }

  function postRequest(){
    let url = document.getElementById("image_url").value;
    let scale_mode = getScaleMultiplier();
    document.getElementById("result").style.display = "none";
    document.getElementById("Failed").innerHTML = " ";
    document.getElementById("ItemPreview").src = " ";
    document.getElementById("bw_example").style.display = "none";
    document.getElementById("us_example").style.display = "none";
    document.getElementById("cf_example").style.display = "none";

    $.ajax({
      method: "POST",
      url: apiUrl,
      dataType: 'json',
      contentType:'application/json',
      data: JSON.stringify({
        "selected_mode" : selected_mode, 
        "scale" : scale_mode, 
        "image_url": url
      }),
      success: function(data){
        if(data.statusCode === 200) {
          document.getElementById("result").style.display = "block";
          document.getElementById("ItemPreview").src = data.image; 
        } else {
          document.getElementById("result").style.display = "block";
          document.getElementById("Failed").innerHTML = "ErrorCode " + data.statusCode + ": " + data.message;
        }
      },
      error: function(textStatus, errorThrown ){
        document.getElementById("result").style.display = "block";
        document.getElementById("Failed").innerHTML = textStatus + " : " + errorThrown;
      }
    }); 
  }