//existing user
document.getElementById("btn").addEventListener("click", userLogin)

function userLogin(e){
    e.preventDefault();

    var xhr_rc = new XMLHttpRequest();

    xhr_rc.open("POST", "/login", true);
    
    

    xhr_rc.onload = function(){
        if(this.status == 200){
            if(this.responseText == "No User"){
                console.log(this.responseText);
                interval_set(this.responseText);            
            } 
            if (this.responseText == 'Wrong Credentials'){
                console.log(this.responseText);
                interval_set(this.responseText);
            }
            if (this.responseText == "Login successful!") {
                console.log(this.responseText);
                setTimeout(css(), 3000);
                readFile();
                }
    }};

    var interval = 1;
    function interval_set(text){
        if(interval == 1){
            var set_interval = setInterval(() => {
            document.getElementById("flash").innerHTML=text;
            document.getElementById("msg").style.display="block";
            interval++;
            if (interval > 5){
                clearInterval(set_interval);
                document.getElementById("uname").value=null;
                document.getElementById("pword").value=null;
                document.getElementById("msg").style.display="none";                   
        }}, 500);    
    }};
                
    function readFile(){
        var xhr1 = new XMLHttpRequest();
        
        
        xhr1.onload = function(){
            if(this.status == 200){
                var csvDetails = JSON.parse(this.responseText);
                console.log(csvDetails);
                for(i=0;i<csvDetails.length;i++){
                    document.getElementById("table").style.display="block";
                    var uid_f = csvDetails[i].UID;
                    var name_f = csvDetails[i].Name;
                    var comment_f = csvDetails[i].Comment;
                    table(name_f, comment_f,uid_f);
                }
        }}
        xhr1.open("GET", "/comments", true);
        xhr1.send();
    }
    
    var log_name = document.getElementById("uname").value;
    var log_pword = document.getElementById("pword").value;

    var log_det = JSON.stringify({"name":log_name, "password": log_pword});

    xhr_rc.send(log_det);
function css(){
    var login = document.getElementById("login").style.display='none';
    var register = document.getElementById("register").style.display='none';
    var comment = document.getElementById("comments").style.display='block';   
};
};

//new user
document.getElementById("btn_new_user").addEventListener("click", newUser);

function newUser(e){
    e.preventDefault();
    var nu_xhr = new XMLHttpRequest();

    nu_xhr.open("POST", "/newuser", true);

    nu_xhr.onload = function(){
        if(this.status == 200){
            if(this.responseText == "User Created!"){
                // document.getElementById("reg_msg").innerHTML = "Please Log In with Your Credentials"
                // setTimeout(function(){
                //     var register = document.getElementById("register").style.display='none';
                // }, 5000);
                console.log(this.responseText);
                interval_set_newUser();
            }
        }};

    var interval_newUser = 1;
    function interval_set_newUser(){
    if(interval_newUser >= 1){
        console.log("initiated")
        var set_interval_newUser = setInterval(() => {
            document.getElementById("reg_msg").innerHTML="Please Log In with Your Credentials";
            document.getElementById("reg_msg_css").style.display="block";
            interval_newUser++;
            if (interval_newUser == 5){
                clearInterval(set_interval_newUser);
                document.getElementById("new_user_name").value=null;
                document.getElementById("new_user_pword").value=null;
                document.getElementById("new_user_confirm_pword").value=null;
                document.getElementById("reg_msg").style.display="none";                   
                document.getElementById("register").style.display="none";                   
    }}, 1000);
    }};

    var name_u = document.getElementById('new_user_name').value;
    var pass_u = document.getElementById('new_user_pword').value;
    var con_pass_u = document.getElementById('new_user_confirm_pword').value;

    var obj = JSON.stringify({"name": name_u, "password":pass_u});
    
    nu_xhr.send(obj)
};


//comments page
document.getElementById("btn1").addEventListener("click", loadComments)

function loadComments(e){  
    e.preventDefault();

    var com = new XMLHttpRequest();

    com.open("POST", "/comments", true);

    com.onload = function(){
        if(this.status == 200){
            console.log(this.responseText);
            var obje = JSON.parse(this.responseText);
            console.log(obje);
            var namecsv = obje.name;
            var commentcsv = obje.comment;
            var uid = obje.UID;
            table(namecsv,commentcsv, uid); 
        }
    }
    var user_name = document.getElementById("name_detail").value;
    var user_comment = document.getElementById("comments_detail").value;

    var log_det = JSON.stringify({"name":user_name, "comment": user_comment});

    com.send(log_det);
    document.getElementById("table").style.display="block";
};

var row = 1; 

function table(name,comment, uid){
    var table =  document.getElementById("table");
    var newRow = table.insertRow(row);
            
    var cell0 = newRow.insertCell(0);
    var cell1 = newRow.insertCell(1);
    var cell2 = newRow.insertCell(2);

    cell0.innerHTML = uid;
    cell1.innerHTML = name;
    cell2.innerHTML = comment;

    row++;        
};

