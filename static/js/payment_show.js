$(document).ready(function () {
    $("input[name='exampleRadios']").change(function () {
        // Tüm collapse'leri gizle
        $(".collapse").collapse("hide");
        
        // Seçilen radio butonun id'sini al
        var selectedOption = $("input[name='exampleRadios']:checked").attr("id");
        
        // İlgili collapse'i göster
        $("#collapseContent" + selectedOption.charAt(selectedOption.length - 1)).collapse("show");
    });
});