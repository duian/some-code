###
# modal
# settings
  title: 头部标题
  remove: 是否获取html弹出，true则不缓存
  width: 弹出层宽度
  button: {value：function(){...}}
###
do ($ = jQuery, UI = jQuery.adama) ->
  $.fn.modal = (options) ->
    settings = $.extend {
      title: ""
      remove: false
      width: 500
      button: false
    }, options
    $defer = $.Deferred()
    self = @
    modalExist = if self.parent().hasClass('modal-body') then true else false
    #创建弹出层
    self.create = () ->
      $('.modal-wrapper').remove() if settings.remove
      #创建弹出层dom结构
      modal = $('<div class="modal-wrapper"><div class="modal"><div class="modal-header"><i class="close"></i><h2></h2></div><div class="modal-body"></div><div class="modal-footer"></div></div></div>')
      #设置标题
      modal.find('.modal-header h2').text settings.title
      #设置内容区宽度
      modal.find('.modal').css {
        'width': settings.width + 'px'
        'margin-left': - settings.width / 2 + 'px'
      }
      #头部icon绑定相对应功能
      modal.find('.modal-header .close').on('click', self.close)

      #是否需要按钮，需要则按需求添加
      if settings.button
        btn = $('<button></button>')
        footer = modal.find('.modal-footer')
        #遍历settings.button项，生成相对应的按钮
        for prop of settings.button
          btn.clone().addClass('btn-small').addClass(if prop is '取消' then 'btn-cancel' else 'btn-confirm').text(prop).on('click', settings.button[prop] ).appendTo(footer)
      modal.appendTo('body')
    #打开弹出层方法
    self.open = () ->
      # if $.browser.msie and $.browser.version < 7
      #   $('html').css {
      #     'overflow': 'hidden'
      #   }
      self.show()
      $('.modal-wrapper').show()

    #关闭弹出层方法
    self.close = () ->
      # $('html').css {
      #   'overflow': 'auto'
      # }
      $('.modal-wrapper').hide()

    #如果modal-wrapper已经存在，则打开弹出层内的内容
    if modalExist
      self.open()
    # 如果modal-wrapper不存在，则创建并显示弹出层内的内容
    else
      self.create()
      self.open()
# class Modal extends View
#   @content:->
#     @div class: 'modal-wrapper', =>
#       @div class: 'modal-header', =>
#         @h2 " "
#         @i class: 'close'
#       @div class: 'modal-body'
#       @div class: 'modal-footer'
#   initialize: ->
#     settings = {
#       title: "sdfsdf"
#       remove: false
#       width: 500
#       button: false
#     }
#     #modalExist = if @parent().hasClass('modal-body') then true else false
#     @create2(settings)

#   create2: (settings) ->
#     @find('.modal-wrapper').remove if settings.remove
#     @find('.modal-header h2').html(settings.title)
#     @find('.modal').css {
#       'width': settings.width + 'px'
#       'margin-left': - settings.width / 2 + 'px'
#     }
#     @find('modal.header .close').on 'click', @close
#   close : () ->
#     $('.modal-wrapper').hide()
#   open :() ->
#     @show()
#     $('.modal-wrapper').show()
# $.extend App.Views, {Modal}