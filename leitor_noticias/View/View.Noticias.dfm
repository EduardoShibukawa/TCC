object fNoticias: TfNoticias
  Left = 0
  Top = 0
  Caption = 'fNoticias'
  ClientHeight = 372
  ClientWidth = 580
  Color = clBtnFace
  Font.Charset = DEFAULT_CHARSET
  Font.Color = clWindowText
  Font.Height = -11
  Font.Name = 'Tahoma'
  Font.Style = []
  OldCreateOrder = False
  PixelsPerInch = 96
  TextHeight = 13
  object dxlytcntrlMain: TdxLayoutControl
    Left = 0
    Top = 0
    Width = 580
    Height = 372
    Align = alClient
    TabOrder = 0
    object lstNoticias: TcxListBox
      Left = 10
      Top = 90
      Width = 279
      Height = 303
      ItemHeight = 13
      TabOrder = 3
      OnClick = lstNoticiasClick
    end
    object mmoConteudo: TcxMemo
      Left = 295
      Top = 200
      Style.BorderColor = clWindowFrame
      Style.BorderStyle = ebs3D
      Style.HotTrack = False
      TabOrder = 7
      Height = 89
      Width = 354
    end
    object btnAbrirXML: TcxButton
      Left = 10
      Top = 10
      Width = 75
      Height = 25
      Caption = 'Abrir CSV'
      TabOrder = 0
      OnClick = btnAbrirXMLClick
    end
    object btnGravarXML: TcxButton
      Left = 91
      Top = 10
      Width = 75
      Height = 25
      Caption = 'Gravar CSV'
      TabOrder = 1
      OnClick = btnGravarXMLClick
    end
    object mmoTitulo: TcxMemo
      Left = 295
      Top = 135
      Lines.Strings = (
        'mmoTitulo')
      Style.BorderColor = clWindowFrame
      Style.BorderStyle = ebs3D
      Style.HotTrack = False
      TabOrder = 6
      Height = 41
      Width = 275
    end
    object ckNegativo: TcxCheckBox
      Left = 414
      Top = 90
      Caption = 'Negativa'
      Style.BorderColor = clWindowFrame
      Style.BorderStyle = ebs3D
      Style.HotTrack = False
      TabOrder = 5
    end
    object edtDataAtualizacao: TcxDateEdit
      Left = 295
      Top = 90
      Style.BorderColor = clWindowFrame
      Style.BorderStyle = ebs3D
      Style.HotTrack = False
      Style.ButtonStyle = bts3D
      Style.PopupBorderStyle = epbsFrame3D
      TabOrder = 4
      Width = 113
    end
    object btnGravarDados: TcxButton
      Left = 10
      Top = 41
      Width = 1
      Height = 25
      Caption = 'btnGravarDados'
      TabOrder = 2
      OnClick = btnGravarDadosClick
    end
    object dxlytcntrlMainGroup_Root: TdxLayoutGroup
      AlignHorz = ahClient
      AlignVert = avClient
      ButtonOptions.Buttons = <>
      Hidden = True
      ShowBorder = False
      Index = -1
    end
    object dxNoticias: TdxLayoutItem
      Parent = dxlytgrpLeft
      AlignHorz = ahClient
      AlignVert = avClient
      CaptionOptions.Text = 'Not'#237'cias'
      CaptionOptions.Layout = clTop
      Control = lstNoticias
      ControlOptions.ShowBorder = False
      Index = 0
    end
    object dxlytgrpLeft: TdxLayoutGroup
      Parent = dxlytgrpBottom
      AlignHorz = ahLeft
      AlignVert = avClient
      CaptionOptions.Text = 'New Group'
      ButtonOptions.Buttons = <>
      ShowBorder = False
      Index = 0
    end
    object dxlytgrpClient: TdxLayoutGroup
      Parent = dxlytgrpBottom
      AlignHorz = ahClient
      AlignVert = avClient
      CaptionOptions.Text = 'New Group'
      ButtonOptions.Buttons = <>
      ShowBorder = False
      Index = 1
    end
    object dxConteudo: TdxLayoutItem
      Parent = dxlytgrpClient
      AlignHorz = ahClient
      AlignVert = avClient
      CaptionOptions.Text = 'Conteudo'
      CaptionOptions.Layout = clTop
      Control = mmoConteudo
      ControlOptions.ShowBorder = False
      Index = 2
    end
    object dxlytgrpTop: TdxLayoutGroup
      Parent = dxlytcntrlMainGroup_Root
      AlignHorz = ahLeft
      AlignVert = avTop
      CaptionOptions.Text = 'New Group'
      ButtonOptions.Buttons = <>
      LayoutDirection = ldHorizontal
      ShowBorder = False
      Index = 0
    end
    object dxlytgrpBottom: TdxLayoutGroup
      Parent = dxlytcntrlMainGroup_Root
      AlignHorz = ahClient
      AlignVert = avClient
      CaptionOptions.Text = 'New Group'
      ButtonOptions.Buttons = <>
      LayoutDirection = ldHorizontal
      ShowBorder = False
      Index = 2
    end
    object dxAbrirXML: TdxLayoutItem
      Parent = dxlytgrpTop
      CaptionOptions.Text = 'cxButton1'
      CaptionOptions.Visible = False
      Control = btnAbrirXML
      ControlOptions.ShowBorder = False
      Index = 0
    end
    object dxGravarXML: TdxLayoutItem
      Parent = dxlytgrpTop
      CaptionOptions.Text = 'cxButton2'
      CaptionOptions.Visible = False
      Control = btnGravarXML
      ControlOptions.ShowBorder = False
      Index = 1
    end
    object dxTitulo: TdxLayoutItem
      Parent = dxlytgrpClient
      AlignHorz = ahClient
      AlignVert = avTop
      CaptionOptions.Text = 'Titulo'
      CaptionOptions.Layout = clTop
      Control = mmoTitulo
      ControlOptions.ShowBorder = False
      Index = 1
    end
    object dxLayoutGroup1: TdxLayoutGroup
      Parent = dxlytgrpClient
      AlignHorz = ahClient
      AlignVert = avTop
      CaptionOptions.Text = 'New Group'
      ButtonOptions.Buttons = <>
      ItemControlAreaAlignment = catNone
      LayoutDirection = ldHorizontal
      ShowBorder = False
      Index = 0
    end
    object dxNegativo: TdxLayoutItem
      Parent = dxLayoutGroup1
      CaptionOptions.Text = ' '
      CaptionOptions.Layout = clTop
      Control = ckNegativo
      ControlOptions.AlignVert = avBottom
      ControlOptions.ShowBorder = False
      Index = 1
    end
    object dxDataAtualizacao: TdxLayoutItem
      Parent = dxLayoutGroup1
      CaptionOptions.Text = 'Data Atualiza'#231#227'o'
      CaptionOptions.Layout = clTop
      Control = edtDataAtualizacao
      ControlOptions.ShowBorder = False
      Index = 0
    end
    object dxLayoutItem1: TdxLayoutItem
      Parent = dxlytcntrlMainGroup_Root
      CaptionOptions.Text = 'cxButton1'
      CaptionOptions.Visible = False
      Control = btnGravarDados
      ControlOptions.ShowBorder = False
      Index = 1
    end
  end
  object OpenDialog: TOpenDialog
    Left = 280
    Top = 8
  end
end
