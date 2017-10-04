object fNoticias: TfNoticias
  Left = 0
  Top = 0
  Caption = 'Leitor de noticias'
  ClientHeight = 885
  ClientWidth = 1272
  Color = clBtnFace
  Font.Charset = DEFAULT_CHARSET
  Font.Color = clWindowText
  Font.Height = -11
  Font.Name = 'Tahoma'
  Font.Style = []
  OldCreateOrder = False
  WindowState = wsMaximized
  PixelsPerInch = 96
  TextHeight = 13
  object dxlytcntrlMain: TdxLayoutControl
    Left = 0
    Top = 0
    Width = 1272
    Height = 885
    Align = alClient
    TabOrder = 0
    ExplicitWidth = 580
    ExplicitHeight = 372
    object lstNoticias: TcxListBox
      Left = 10
      Top = 90
      Width = 575
      Height = 785
      ItemHeight = 13
      TabOrder = 3
      OnClick = lstNoticiasClick
    end
    object btnAbrirJSON: TcxButton
      Left = 10
      Top = 10
      Width = 95
      Height = 25
      Hint = 'CTRL + O'
      Action = actAbrirJSON
      ParentShowHint = False
      ShowHint = True
      TabOrder = 0
    end
    object btnGravarCSV: TcxButton
      Left = 111
      Top = 10
      Width = 82
      Height = 25
      Hint = 'CTRL + G'
      Action = actGravarCSV
      ParentShowHint = False
      ShowHint = True
      TabOrder = 1
    end
    object mmoTitulo: TcxMemo
      Left = 591
      Top = 135
      Lines.Strings = (
        'mmoTitulo')
      Style.BorderColor = clWindowFrame
      Style.BorderStyle = ebs3D
      Style.HotTrack = False
      TabOrder = 6
      Height = 34
      Width = 967
    end
    object rgSentimento: TcxRadioGroup
      Left = 703
      Top = 72
      Caption = 'Sentimento'
      Properties.Columns = 3
      Properties.Items = <
        item
          Caption = 'Negativo'
          Value = 0
        end
        item
          Caption = 'Neutro'
          Value = 2
        end
        item
          Caption = 'Positivo'
          Value = 1
        end>
      Style.BorderColor = clWindowFrame
      Style.BorderStyle = ebs3D
      TabOrder = 5
      Height = 36
      Width = 226
    end
    object btnGravarDados: TcxButton
      Left = 10
      Top = 41
      Width = 95
      Height = 25
      Hint = 'F1'
      Action = actGravarDados
      ParentShowHint = False
      ShowHint = True
      TabOrder = 2
    end
    object mmoConteudo: TcxMemo
      Left = 591
      Top = 193
      Style.BorderColor = clWindowFrame
      Style.BorderStyle = ebs3D
      Style.HotTrack = False
      TabOrder = 7
      Height = 89
      Width = 354
    end
    object edtDataAtualizacao: TcxDateEdit
      Left = 591
      Top = 90
      Style.BorderColor = clWindowFrame
      Style.BorderStyle = ebs3D
      Style.HotTrack = False
      Style.ButtonStyle = bts3D
      Style.PopupBorderStyle = epbsFrame3D
      TabOrder = 4
      Width = 106
    end
    object dxlytcntrlMainGroup_Root: TdxLayoutGroup
      AlignHorz = ahClient
      AlignVert = avClient
      CaptionOptions.Visible = False
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
      CaptionOptions.Visible = False
      ButtonOptions.Buttons = <>
      ShowBorder = False
      Index = 0
    end
    object dxlytgrpClient: TdxLayoutGroup
      Parent = dxlytgrpBottom
      AlignHorz = ahClient
      AlignVert = avClient
      CaptionOptions.Text = 'New Group'
      CaptionOptions.Visible = False
      ButtonOptions.Buttons = <>
      ShowBorder = False
      Index = 1
    end
    object dxlytgrpTop: TdxLayoutGroup
      Parent = dxlytcntrlMainGroup_Root
      AlignHorz = ahLeft
      AlignVert = avTop
      CaptionOptions.Text = 'New Group'
      CaptionOptions.Visible = False
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
      CaptionOptions.Visible = False
      ButtonOptions.Buttons = <>
      LayoutDirection = ldHorizontal
      ShowBorder = False
      Index = 2
    end
    object dxAbrirXML: TdxLayoutItem
      Parent = dxlytgrpTop
      CaptionOptions.Text = 'cxButton1'
      CaptionOptions.Visible = False
      Control = btnAbrirJSON
      ControlOptions.ShowBorder = False
      Index = 0
    end
    object dxGravarXML: TdxLayoutItem
      Parent = dxlytgrpTop
      CaptionOptions.Text = 'cxButton2'
      CaptionOptions.Visible = False
      Control = btnGravarCSV
      ControlOptions.ShowBorder = False
      Index = 1
    end
    object dxTitulo: TdxLayoutItem
      Parent = dxlytgrpClient
      AlignHorz = ahClient
      CaptionOptions.Text = 'Titulo'
      CaptionOptions.Layout = clTop
      Control = mmoTitulo
      ControlOptions.ShowBorder = False
      Index = 1
    end
    object dxSentimento: TdxLayoutItem
      Parent = dxLayoutGroup1
      AlignHorz = ahLeft
      CaptionOptions.Text = 'cxRadioGroup1'
      CaptionOptions.Visible = False
      CaptionOptions.Layout = clTop
      Control = rgSentimento
      ControlOptions.ShowBorder = False
      Index = 1
    end
    object dxGravarDados: TdxLayoutItem
      Parent = dxlytcntrlMainGroup_Root
      AlignHorz = ahLeft
      CaptionOptions.Text = 'cxButton1'
      CaptionOptions.Visible = False
      Control = btnGravarDados
      ControlOptions.ShowBorder = False
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
    object dxLayoutGroup1: TdxLayoutGroup
      Parent = dxlytgrpClient
      CaptionOptions.Text = 'New Group'
      ButtonOptions.Buttons = <>
      LayoutDirection = ldHorizontal
      ShowBorder = False
      Index = 0
    end
    object dxDataAtualizacao: TdxLayoutItem
      Parent = dxLayoutGroup1
      CaptionOptions.Text = 'Data Atualiza'#231#227'o'
      CaptionOptions.Layout = clTop
      Control = edtDataAtualizacao
      ControlOptions.ShowBorder = False
      Index = 0
    end
  end
  object OpenDialog: TOpenDialog
    Filter = 'JSON|*.json|Todos Arquivos|*.*'
    Left = 784
    Top = 16
  end
  object actlstList: TActionList
    Left = 880
    Top = 16
    object actAbrirJSON: TAction
      Caption = 'Abrir JSON'
      ShortCut = 16463
      OnExecute = actAbrirJSONExecute
    end
    object actGravarCSV: TAction
      Caption = 'Gravar CSV'
      ShortCut = 16455
      OnExecute = actGravarCSVExecute
    end
    object actGravarDados: TAction
      Caption = 'Gravar Dados'
      ShortCut = 112
      OnExecute = actGravarDadosExecute
    end
  end
end
