    // Bireysel checkbox
    $('#bireysel').change(function() {
        if ($(this).is(':checked')) {
            $('#kurumsal').prop('checked', false); // Kurumsal checkbox'un seçili özelliğini kaldır
            $('#kurumsalCollapse').collapse('hide'); // Kurumsal collapse'i gizle
            $('#bireyselCollapse').collapse('show'); // Bireysel collapse'i göster
        } else {
            $('#bireyselCollapse').collapse('hide'); // Bireysel checkbox iptal edilirse, Bireysel collapse'i gizle
        }
    });

    // Kurumsal checkbox
    $('#kurumsal').change(function() {
        if ($(this).is(':checked')) {
            $('#bireysel').prop('checked', false); // Bireysel checkbox'un seçili özelliğini kaldır
            $('#bireyselCollapse').collapse('hide'); // Bireysel collapse'i gizle
            $('#kurumsalCollapse').collapse('show'); // Kurumsal collapse'i göster
        } else {
            $('#kurumsalCollapse').collapse('hide'); // Kurumsal checkbox iptal edilirse, Kurumsal collapse'i gizle
        }
    });