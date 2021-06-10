function deleteBlog(blogID)
{
    fetch('/delete-Blog',
    {
        method:"POST",
        body:JSON.stringify({blogID : blogID})
    }).then((_res)=>{
        window.location.href='/';
    });
}