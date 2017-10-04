unit View.Noticias;

interface

uses
  Winapi.Windows, Winapi.Messages, System.SysUtils, System.Variants, System.Classes, Vcl.Graphics,
  Vcl.Controls, Vcl.Forms, Vcl.Dialogs, cxGraphics, cxControls, cxLookAndFeels,
  cxLookAndFeelPainters, Vcl.Menus, dxLayoutControlAdapters, dxLayoutContainer,
  dxLayoutcxEditAdapters, cxContainer, cxEdit, Vcl.ComCtrls, dxCore, cxDateUtils, cxCheckBox,
  cxMemo, cxTextEdit, cxMaskEdit, cxDropDownEdit, cxCalendar, cxListBox, Vcl.StdCtrls, cxButtons,
  cxClasses, dxLayoutControl, Pattern.Aggregate, Pattern.Abstraction, Pattern.ConcreteImplementorCSV,
  Pattern.RefinedAbstraction.Noticia, Model.Noticia, cxGroupBox, cxRadioGroup, System.Actions,
  Vcl.ActnList;

type
  TfNoticias = class(TForm)
    dxlytcntrlMainGroup_Root: TdxLayoutGroup;
    dxlytcntrlMain: TdxLayoutControl;
    btnAbrirJSON: TcxButton;
    dxAbrirXML: TdxLayoutItem;
    btnGravarCSV: TcxButton;
    dxGravarXML: TdxLayoutItem;
    lstNoticias: TcxListBox;
    dxNoticias: TdxLayoutItem;
    edtDataAtualizacao: TcxDateEdit;
    dxDataAtualizacao: TdxLayoutItem;
    mmoConteudo: TcxMemo;
    dxConteudo: TdxLayoutItem;
    dxlytgrpClient: TdxLayoutGroup;
    dxlytgrpLeft: TdxLayoutGroup;
    dxlytgrpTop: TdxLayoutGroup;
    dxlytgrpBottom: TdxLayoutGroup;
    OpenDialog: TOpenDialog;
    mmoTitulo: TcxMemo;
    dxTitulo: TdxLayoutItem;
    btnGravarDados: TcxButton;
    dxGravarDados: TdxLayoutItem;
    rgSentimento: TcxRadioGroup;
    dxSentimento: TdxLayoutItem;
    actlstList: TActionList;
    actAbrirJSON: TAction;
    actGravarCSV: TAction;
    actGravarDados: TAction;
    dxLayoutGroup1: TdxLayoutGroup;
    procedure lstNoticiasClick(Sender: TObject);
    procedure actAbrirJSONExecute(Sender: TObject);
    procedure actGravarCSVExecute(Sender: TObject);
    procedure actGravarDadosExecute(Sender: TObject);
  private
    { Private declarations }
    FAggregate: IAggregate<TNoticia>;
    procedure CarregarDadosNoticia;

    procedure GravaDadosNoticia;

    procedure CarregarCSV;
    procedure GravarCSV;
  public
    { Public declarations }
  end;

var
  fNoticias: TfNoticias;

implementation

uses Pattern.ConcreteAggregateCSV, Pattern.Iterator;

{$R *.dfm}

{ TfNoticias }

procedure TfNoticias.actAbrirJSONExecute(Sender: TObject);
begin
  CarregarCSV;
  lstNoticias.ItemIndex := 0;
  CarregarDadosNoticia;
end;

procedure TfNoticias.actGravarCSVExecute(Sender: TObject);
begin
  GravarCSV;
end;

procedure TfNoticias.actGravarDadosExecute(Sender: TObject);
begin
  if Assigned(FAggregate)
    and (FAggregate.GetLista.Count > 0) then
    GravaDadosNoticia;
end;

procedure TfNoticias.CarregarCSV;
var
  Iterator: IIterator<TNoticia>;
begin
  if Assigned(FAggregate) then
    FAggregate := nil;

  if OpenDialog.Execute() then
  begin
    FAggregate := TConcreteAggregateCSV.Create(OpenDialog.FileName);

    Iterator := FAggregate.GetIterator;

    lstNoticias.Clear;
    Iterator.PrimeiroObjeto;
    while not Iterator.FimLista do
    begin
      lstNoticias.Items.Add(Format(
       '%s - %s', [
       FormatDateTime('dd/mm/yyyy', Iterator.ObjetoAtual.DataAtualizacao),
       Iterator.ObjetoAtual.Titulo
      ]));
      Iterator.ProximoObjeto;
    end;

    lstNoticias.ItemIndex := 0;
  end;
end;

procedure TfNoticias.CarregarDadosNoticia;
var
  Iterator: IIterator<TNoticia>;
  aNoticia: TNoticia;
begin
  Iterator := FAggregate.GetIterator;

  aNoticia := Iterator.Buscar(lstNoticias.ItemIndex);

  edtDataAtualizacao.Date := aNoticia.DataAtualizacao;
  mmoTitulo.Text := aNoticia.Titulo;
  mmoConteudo.Text := aNoticia.Conteudo;
  rgSentimento.EditValue := Integer(aNoticia.Sentimento);
end;

procedure TfNoticias.GravaDadosNoticia;
var
  Iterator: IIterator<TNoticia>;
  aNoticia: TNoticia;
begin
  Iterator := FAggregate.GetIterator;

  aNoticia := Iterator.Buscar(lstNoticias.ItemIndex);

  aNoticia.DataAtualizacao := edtDataAtualizacao.Date;
  aNoticia.Titulo := mmoTitulo.Text;
  aNoticia.Conteudo := mmoConteudo.Text;
  aNoticia.Sentimento := TSentimento(rgSentimento.EditValue);
end;

procedure TfNoticias.GravarCSV;
var
  Exportador: IExportador<TNoticia>;
begin
  Exportador := TExportadorNoticia.Create(TFormatoCSV.Create);
  try
    Exportador.ExportarDados(FAggregate.GetLista.ToArray);
  finally
    Exportador := nil;
  end;
end;

procedure TfNoticias.lstNoticiasClick(Sender: TObject);
begin
  if lstNoticias.Items.Count = 0 then
    Exit;

  CarregarDadosNoticia;
end;

end.


