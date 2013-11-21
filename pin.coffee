do ($ = jQuery, UI = jQuery.adama) ->
  $.fn.pin = (options) ->
    scrollY = 0
    elements = []
    disables = false
    $window = $(window)
    options = options or {}

    recalculateLimits: ->
      for i in elements
        $this = i
        if options.minWidth and $window.width() <= options.minWidth
          if $this.parent().is('.pin-wrapper')
            $this.unwrap()
          $this.css({
            width: ""
            left: ""
            top: ""
            position: ""
          })
          if options.activeClass
            $this.removeClass(activeClass)
          disabled = true
          continue
        else
          disabled = false

        $container = options.containerSelector or $this.closet(options.containerSelector)
        offset = $this.offset()
        containerOffset = $container.offset()
        parentOffset = $this.offsetParent().offset()

        unless $this.parent().is('pin-wrapper')
          $this.wrap('<div class="pin-wrapper">')

        $.data('pin',{
          from : $container.offset().top
          to : $container.offset().top + $container.outerHeight() - $this.outerHeight()
          end : $container.offset().top + $container.outerHeight()
        })

        $this.css({width: $this.outerWidth()})
        $this.parent.css('height',$this.outerHeight())
    onScroll: ->
      scrollY = $window.scrollTop()
      for i in elements
        $this = $i
        data = $this.data('pin')
        from = data.from
        to = data.to
        if data.end < scrollY
          $this.css({
            left: ""
            top: ""
            position: "absolute"
          })
        else if from < scrollY and scrollY < to
          $this.css({
            left: $containerOffse.left + $container.outerHeight() - offset.left
            top: 0
            position: "fixed"
          })
        else

