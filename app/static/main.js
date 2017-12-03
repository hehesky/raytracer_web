
function check_form()
    {
        var p1,p2,u;
        u=document.getElementById("username");  
        p1=document.getElementById("password");
        p2=document.getElementById("password_confirm");
        if(u.value=='')
        {
            document.getElementById("password_warning").innerHTML="Username cannot be empty";
            return false;
        }
        if(p1.value!=p2.value )
        {
            document.getElementById("password_warning").innerHTML="Passwords do not match.";
            return false;
        }
        if(p1.value.length<=3)
        {
            document.getElementById("password_warning").innerHTML="Password too short. At least 4 characters.";
            return false;
        }
}