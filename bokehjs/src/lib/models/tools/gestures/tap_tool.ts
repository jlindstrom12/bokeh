import {SelectTool, SelectToolView} from "./select_tool"
import type {CallbackLike1} from "../../callbacks/callback"
import type * as p from "core/properties"
import type {TapEvent, KeyModifiers} from "core/ui_events"
import * as events from "core/bokeh_events"
import type {PointGeometry} from "core/geometry"
import type {SelectionMode} from "core/enums"
import {TapBehavior, TapGesture} from "core/enums"
import type {ColumnarDataSource} from "../../sources/columnar_data_source"
import type {DataRendererView} from "../../renderers/data_renderer"
import {tool_icon_tap_select} from "styles/icons.css"

export type TapToolCallback = CallbackLike1<TapTool, {
  geometries: (PointGeometry & {x: number, y: number})[]
  source: ColumnarDataSource
  event: {
    modifiers?: KeyModifiers
  }
}>

export class TapToolView extends SelectToolView {
  declare model: TapTool

  override _tap(ev: TapEvent): void {
    if (this.model.gesture == "tap") {
      this._handle_tap(ev)
    }
  }

  override _doubletap(ev: TapEvent): void {
    if (this.model.gesture == "doubletap") {
      this._handle_tap(ev)
    }
  }

  _handle_tap(ev: TapEvent): void {
    const handle_event = (() => {
      const {modifiers} = this.model
      if (modifiers.shift != null && modifiers.shift != ev.modifiers.shift) {
        return false
      }
      if (modifiers.ctrl != null && modifiers.ctrl != ev.modifiers.ctrl) {
        return false
      }
      if (modifiers.alt != null && modifiers.alt != ev.modifiers.alt) {
        return false
      }
      return true
    })()

    if (!handle_event) {
      return
    }

    const {sx, sy} = ev
    const {frame} = this.plot_view
    if (!frame.bbox.contains(sx, sy)) {
      return
    }

    this._clear_other_overlays()

    const geometry: PointGeometry = {type: "point", sx, sy}
    const {modifiers} = ev
    const mode = this._select_mode(modifiers)

    switch (this.model.behavior) {
      case "select": {
        this._select(geometry, true, mode, modifiers)
        break
      }
      case "inspect": {
        this._inspect(geometry, true, mode, modifiers)
        break
      }
    }
  }

  protected _select(geometry: PointGeometry, final: boolean, mode: SelectionMode, modifiers?: KeyModifiers): void {
    const renderers_by_source = this._computed_renderers_by_data_source()

    for (const [source, renderers] of renderers_by_source) {
      const renderer_views = renderers
        .map((r) => this.plot_view.renderer_view(r))
        .filter((rv): rv is DataRendererView => rv != null)
      const did_hit = source.selection_manager.select(renderer_views, geometry, final, mode)
      if (did_hit) {
        this._emit_callback(renderer_views, geometry, source, modifiers)
      }
    }

    this._emit_selection_event(geometry)
    this.plot_view.state.push("tap", {selection: this.plot_view.get_selection()})
  }

  protected _inspect(geometry: PointGeometry, final: boolean, mode: SelectionMode, modifiers?: KeyModifiers): void {
    const renderers_by_source = this._computed_renderers_by_data_source()

    for (const [source, renderers] of renderers_by_source) {
      const renderer_views = renderers
        .map((r) => this.plot_view.renderer_view(r))
        .filter((rv): rv is DataRendererView => rv != null)
      const did_hit = source.selection_manager.inspect(renderer_views, geometry, final, mode)
      if (did_hit) {
        this._emit_callback(renderer_views, geometry, source, modifiers)
      }
    }
  }

  protected _emit_callback(renderer_views: DataRendererView[], geometry: PointGeometry, source: ColumnarDataSource, modifiers?: KeyModifiers): void {
    const {callback} = this.model
    if (callback != null && renderer_views.length != 0) {
      const geometries = renderer_views.map((rv) => {
        const x = rv.coordinates.x_scale.invert(geometry.sx)
        const y = rv.coordinates.y_scale.invert(geometry.sy)
        return {...geometry, x, y}
      })
      const data = {
        geometries,
        source,
        event: {modifiers},
      }
      callback.execute(this.model, data)
    }
  }
}

export namespace TapTool {
  export type Attrs = p.AttrsOf<Props>

  export type Props = SelectTool.Props & {
    behavior: p.Property<TapBehavior>
    gesture: p.Property<TapGesture>
    modifiers: p.Property<events.KeyModifiers>
    callback: p.Property<TapToolCallback | null>
  }
}

export interface TapTool extends TapTool.Attrs {}

export class TapTool extends SelectTool {
  declare properties: TapTool.Props
  declare __view_type__: TapToolView

  constructor(attrs?: Partial<TapTool.Attrs>) {
    super(attrs)
  }

  static {
    this.prototype.default_view = TapToolView

    this.define<TapTool.Props>(({Any, Nullable}) => ({
      behavior:  [ TapBehavior, "select" ],
      gesture:   [ TapGesture, "tap"],
      modifiers: [ events.KeyModifiers, {} ],
      callback:  [ Nullable(Any /*TODO*/), null ],
    }))

    this.register_alias("click", () => new TapTool({behavior: "inspect"}))
    this.register_alias("tap", () => new TapTool())
    this.register_alias("doubletap", () => new TapTool({gesture: "doubletap"}))
  }

  override tool_name = "Tap"
  override tool_icon = tool_icon_tap_select
  override event_type = "tap" as "tap"
  override default_order = 10
}
