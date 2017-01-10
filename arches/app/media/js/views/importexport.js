require([
    'jquery',
    'knockout',
    'underscore',
    'arches',
    'views/base-manager'
], function($, ko, _, arches, BaseManagerView) {
    var ImportExportView = BaseManagerView.extend({
       initialize: function(options) {
           BaseManagerView.prototype.initialize.call(this, options);
       }
   });
   return new ImportExportView();
    // $(document).ready(function() {
        // this.dropzoneOptions = {
        //     url: "/",
        //     dictDefaultMessage: '',
        //     autoProcessQueue: false,
        //     previewTemplate: $("template#file-widget-dz-preview").html(),
        //     autoQueue: false,
        //     previewsContainer: ".dz-previews." + this.uniqueidClass(),
        //     clickable: ".fileinput-button." + this.uniqueidClass(),
        //     acceptedFiles: this.acceptedFiles(),
        //     maxFilesize: this.maxFilesize(),
        //     init: function() {
        //         self.dropzone = this;
        //
        //         this.on("addedfile", function(file) {
        //             self.filesForUpload.push(file);
        //         });
        //
        //         this.on("error", function(file, error) {
        //             file.error = error;
        //             self.filesForUpload.valueHasMutated()
        //         });
        //
        //         this.on("removedfile", function(file) {
        //             self.filesForUpload.remove(file);
        //         });
        //     }
        // };
    //});
});
