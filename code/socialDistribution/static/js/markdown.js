/* 
Takes in text input and renders it to markdown format, which is displayed. 
*/

$(document).ready(function(){
    $(".content-markdown").each(function(){
      var content = $(this).text()
      var markedContent = marked(content)
      $(this).html(markedContent)
    })
  })
