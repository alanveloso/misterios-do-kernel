#import "../config.typ": *

#let overflow-ids = state("overflow-ids", ())
#let fonte-serif = "Libertinus Serif"
#let fonte-sans = ("Liberation Sans", "DejaVu Sans", "Noto Sans")
#let altura-rodape = 12mm
#let zona-titulo = 16mm
#let altura-conteudo = 42mm

#let categoria-rotulo(categoria) = {
  upper(str(categoria).replace("-", " "))
}

#let conceito-rodape(conceitos) = {
  if type(conceitos) != array or conceitos.len() == 0 {
    return ""
  }
  let primeiro = conceitos.at(0)
  if primeiro == none or str(primeiro).trim() == "" {
    return ""
  }
  upper(str(primeiro))
}

#let marca() = {
  align(center, text(
    font: fonte-sans,
    size: 6pt,
    weight: "semibold",
    tracking: 1.35pt,
    fill: color-ink,
    [MISTÉRIOS DO KERNEL],
  ))
}

#let titulo-bloco(titulo) = {
  block(width: 100%, height: zona-titulo, clip: true, {
    set align(center + horizon)
    set par(leading: 0.82em)
    box(width: 78%, {
      text(
        font: fonte-serif,
        size: 13pt,
        weight: "bold",
        fill: color-ink,
        hyphenate: false,
        titulo,
      )
    })
  })
}

#let frente-corpo(enigma, size) = {
  set par(justify: false, leading: 0.92em)
  align(center, box(width: 86%, {
    text(font: fonte-serif, size: size, fill: color-ink, weight: "regular", enigma)
  }))
}

#let verso-corpo(solucao, size) = {
  align(center, text(
    font: fonte-sans,
    size: 6.5pt,
    weight: "semibold",
    tracking: 1.7pt,
    fill: color-accent,
    [SOLUÇÃO],
  ))
  v(0.4em)
  set par(justify: false, leading: 0.88em)
  align(center, box(width: 86%, {
    text(font: fonte-serif, size: size, fill: color-ink, weight: "regular", solucao)
  }))
}

#let ajustar(id, max-w, max-h, builder) = {
  context {
    let tamanhos = (10pt, 9.5pt, 9pt, 8.5pt, 8pt, 7.5pt)
    let escolhido = none
    let coube = false
    for size in tamanhos {
      let corpo = builder(size)
      let medido = measure(block(width: max-w, corpo))
      if medido.height <= max-h {
        escolhido = corpo
        coube = true
        break
      }
    }
    if not coube {
      overflow-ids.update(ids => if id in ids { ids } else { ids + (id,) })
      escolhido = builder(7.5pt)
    }
    block(width: max-w, height: max-h, clip: true, escolhido)
  }
}

#let rodape(categoria, conceitos, id, face) = {
  set text(font: fonte-sans, size: 6.2pt, weight: "semibold")
  let esquerda = if face == "frente" {
    categoria-rotulo(categoria)
  } else {
    conceito-rodape(conceitos)
  }
  grid(
    columns: (1fr, auto, 1fr),
    align: (left + horizon, center + horizon, right + horizon),
    [],
    text(fill: color-accent, tracking: 0.6pt, esquerda),
    text(fill: color-ink, id),
  )
}

#let card(
  id: none,
  titulo: none,
  categoria: none,
  enigma: none,
  solucao: none,
  conceitos: (),
  autoria: (),
  referencias: (),
  face: "frente",
) = {
  let inner-w = card-width - card-margin-left - card-margin-right
  let builder = if face == "verso" {
    size => verso-corpo(solucao, size)
  } else {
    size => frente-corpo(enigma, size)
  }

  block(
    width: card-width,
    height: card-height,
    fill: color-bg,
    clip: false,
    {
      place(top + left, image(
        mask-path,
        width: card-width,
        height: card-height,
        fit: "stretch",
      ))

      block(
        width: card-width,
        height: card-height - altura-rodape,
        clip: true,
        inset: (
          left: card-margin-left,
          right: card-margin-right,
          top: card-margin-top,
          bottom: 0mm,
        ),
        {
          marca()
          v(2.4em)
          titulo-bloco(titulo)
          v(2.2em)
          ajustar(id, inner-w, altura-conteudo, builder)
        },
      )

      place(bottom, block(
        width: card-width,
        height: altura-rodape,
        inset: (
          left: card-margin-left,
          right: card-margin-right,
          top: 0mm,
          bottom: 0mm,
        ),
        align(horizon, rodape(categoria, conceitos, id, face)),
      ))
    },
  )
}

#let relatorio-overflow() = {
  context {
    let ids = overflow-ids.final()
    if ids.len() > 0 {
      panic(
        "Cartas que não couberam na área de conteúdo (texto não entra no rodapé): "
          + ids.join(", "),
      )
    }
  }
}
