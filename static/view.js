
$(document).ready(function() {
    $('td').blur(function() {
        var cellContent = $(this).text();
        var originalContent = $(this).attr('original')
        if (originalContent === cellContent ) return;

        var $row = $(this).parent();
        var $table = $row.parent();
        var rowIndex = $row.index();
        var columnIndex = $(this).index();
        console.log(`"Cell content at ${rowIndex}:${columnIndex} is ${cellContent}`);
    });
    $('td').on('keydown', function(event) {
        if (event.keyCode === 13) {
            event.preventDefault();
            $(this).blur();
        }
    });
});