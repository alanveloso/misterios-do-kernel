#import "config.typ": card-width, card-height, color-bg
#import "components/card.typ": card, relatorio-overflow

#let historias = json("/build/historias.json")

#set page(width: card-width, height: card-height, margin: 0pt, fill: color-bg)
#set text(lang: "pt", fill: rgb("#1a1714"))

#for (i, h) in historias.enumerate() {
  if i > 0 {
    pagebreak()
  }
  card(
    id: h.at("id"),
    titulo: h.at("titulo"),
    categoria: h.at("categoria"),
    enigma: h.at("enigma"),
    solucao: h.at("solucao"),
    conceitos: h.at("conceitos", default: ()),
    autoria: h.at("autoria", default: ()),
    referencias: h.at("referencias", default: ()),
    face: "frente",
  )
  pagebreak()
  card(
    id: h.at("id"),
    titulo: h.at("titulo"),
    categoria: h.at("categoria"),
    enigma: h.at("enigma"),
    solucao: h.at("solucao"),
    conceitos: h.at("conceitos", default: ()),
    autoria: h.at("autoria", default: ()),
    referencias: h.at("referencias", default: ()),
    face: "verso",
  )
}

#relatorio-overflow()
