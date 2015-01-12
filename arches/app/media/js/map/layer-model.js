define([
    'underscore'
], function(_) {
    return function(config) {
        var layerModel = {
                layer: null,
                id: _.uniqueId('layer_'),
                icon: "",
                name: "",
                description: "",
                categories: [],
                onMap: false,
                iconColor: "#000000"
            };
        _.extend(layerModel, config);
        return layerModel;
    }
});