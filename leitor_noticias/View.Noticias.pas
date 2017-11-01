unit View.Noticias;

interface

uses
  Winapi.Windows, Winapi.Messages, System.SysUtils, System.Variants, System.Classes, Vcl.Graphics,
  Vcl.Controls, Vcl.Forms, Vcl.Dialogs, cxGraphics, cxControls, cxLookAndFeels,
  cxLookAndFeelPainters, Vcl.Menus, dxLayoutControlAdapters, dxLayoutContainer,
  dxLayoutcxEditAdapters, cxContainer, cxEdit, Vcl.ComCtrls, dxCore, cxDateUtils, cxCheckBox,
  cxMemo, cxTextEdit, cxMaskEdit, cxDropDownEdit, cxCalendar, cxListBox, Vcl.StdCtrls, cxButtons,
  cxClasses, dxLayoutControl, Pattern.Aggregate, Pattern.Abstraction, Pattern.ConcreteImplementorCSV,
  Pattern.RefinedAbstraction.Noticia, Model.Noticia;

type
  TfNoticias = class(TForm)
    dxlytcntrlMainGroup_Root: TdxLayoutGroup;
    dxlytcntrlMain: TdxLayoutControl;
    btnAbrirXML: TcxButton;
    dxAbrirXML: TdxLayoutItem;
    btnGravarXML: TcxButton;
    dxGravarXML: TdxLayoutItem;
    lstNoticias: TcxListBox;
    dxNoticias: TdxLayoutItem;
    edtDataAtualizacao: TcxDateEdit;
    dxDataAtualizacao: TdxLayoutItem;
    mmoConteudo: TcxMemo;
    dxConteudo: TdxLayoutItem;
    ckNegativo: TcxCheckBox;
    dxNegativo: TdxLayoutItem;
    dxlytgrpClient: TdxLayoutGroup;
    dxlytgrpLeft: TdxLayoutGroup;
    dxlytgrpTop: TdxLayoutGroup;
    dxlytgrpBottom: TdxLayoutGroup;
    OpenDialog: TOpenDialog;
    mmoTitulo: TcxMemo;
    dxTitulo: TdxLayoutItem;
    dxLayoutGroup1: TdxLayoutGroup;
    btnGravarDados: TcxButton;
    dxLayoutItem1: TdxLayoutItem;
    procedure lstNoticiasClick(Sender: TObject);
    procedure btnAbrirXMLClick(Sender: TObject);
    procedure btnGravarXMLClick(Sender: TObject);
    procedure btnGravarDadosClick(Sender: TObject);
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

procedure TfNoticias.btnAbrirXMLClick(Sender: TObject);
begin
  CarregarCSV;
  CarregarDadosNoticia;
end;

procedure TfNoticias.btnGravarDadosClick(Sender: TObject);
begin
  if Assigned(FAggregate)
    and (FAggregate.GetLista.Count > 0) then
    GravaDadosNoticia;
end;

procedure TfNoticias.btnGravarXMLClick(Sender: TObject);
begin
  GravarCSV;
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

    //FAggregate := TConcreteAggregateCSV.Create('K:\UEM\TCC\Noticias\dados\items_g1_noticias_9.json');

    Iterator := FAggregate.GetIterator;

    lstNoticias.Clear;

    Iterator.PrimeiroObjeto;
    while not Iterator.FimLista do
    begin
      Iterator.ProximoObjeto;
      lstNoticias.Items.Add(Format(
       '%s - %s', [
       FormatDateTime('yyyyy/mm/dd', Iterator.ObjetoAtual.DataAtualizacao),
       Iterator.ObjetoAtual.Titulo
      ]));
    end;
  end;
end;

procedure TfNoticias.CarregarDadosNoticia;
var
  Iterator: IIterator<TNoticia>;
  aNoticia: TNoticia;
begin
  Iterator := FAggregate.GetIterator;

  aNoticia := Iterator.Buscar(lstNoticias.ItemIndex + 1);

  edtDataAtualizacao.Date := aNoticia.DataAtualizacao;
  mmoTitulo.Text := aNoticia.Titulo;
  mmoConteudo.Text := aNoticia.Conteudo;
  ckNegativo.Checked := aNoticia.Sentimento = senNegativo;
end;

procedure TfNoticias.GravaDadosNoticia;
var
  Iterator: IIterator<TNoticia>;
  aNoticia: TNoticia;
begin
  Iterator := FAggregate.GetIterator;

  aNoticia := Iterator.Buscar(lstNoticias.ItemIndex + 1);

  aNoticia.DataAtualizacao := edtDataAtualizacao.Date;
  aNoticia.Titulo := mmoTitulo.Text;
  aNoticia.Conteudo := mmoConteudo.Text;
  if ckNegativo.Checked then
    aNoticia.Sentimento := senNegativo
  else aNoticia.Sentimento := senPositivo;
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
