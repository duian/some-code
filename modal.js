/*
# modal
# settings
  title: 头部标题
  remove: 是否获取html弹出，true则不缓存
  width: 弹出层宽度
  button: {value：function(){...}}
*/


(function() {
  (function($, UI) {
    return $.fn.modal = function(options) {
      var $defer, modalExist, self, settings;
      settings = $.extend({
        title: "",
        remove: false,
        width: 500,
        button: false
      }, options);
      $defer = $.Deferred();
      self = this;
      modalExist = self.parent().hasClass('modal-body') ? true : false;
      self.create = function() {
        var btn, footer, modal, prop;
        if (settings.remove) {
          $('.modal-wrapper').remove();
        }
        modal = $('<div class="modal-wrapper"><div class="modal"><div class="modal-header"><i class="close"></i><h2></h2></div><div class="modal-body"></div><div class="modal-footer"></div></div></div>');
        modal.find('.modal-header h2').text(settings.title);
        modal.find('.modal').css({
          'width': settings.width + 'px',
          'margin-left': -settings.width / 2 + 'px'
        });
        modal.find('.modal-header .close').on('click', self.close);
        if (settings.button) {
          btn = $('<button></button>');
          footer = modal.find('.modal-footer');
          for (prop in settings.button) {
            btn.clone().addClass('btn-small').addClass(prop === '取消' ? 'btn-cancel' : 'btn-confirm').text(prop).on('click', settings.button[prop]).appendTo(footer);
          }
        }
        return modal.appendTo('body');
      };
      self.open = function() {
        self.show();
        return $('.modal-wrapper').show();
      };
      self.close = function() {
        return $('.modal-wrapper').hide();
      };
      if (modalExist) {
        return self.open();
      } else {
        self.create();
        return self.open();
      }
    };
  })(jQuery, jQuery.adama);

}).call(this);
