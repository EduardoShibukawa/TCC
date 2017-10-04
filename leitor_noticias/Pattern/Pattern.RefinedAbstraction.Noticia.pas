unit Pattern.RefinedAbstraction.Noticia;

interface

uses
  Pattern.Abstraction, Pattern.Implementor, Model.Noticia;

type
  { Refined Abstraction }
  TExportadorNoticia = class(TInterfacedObject, IExportador<TNoticia>)
  private
    FFormato: IFormato;
    procedure EscreverCabecalho;
  public
    constructor Create(Formato: IFormato);
    procedure ExportarDados(const Dados: TArray<TNoticia>);
  end;

implementation

uses
  SysUtils, DBClient;

{ TExportadorProdutos }

constructor TExportadorNoticia.Create(Formato: IFormato);
begin
  FFormato := Formato;
end;

procedure TExportadorNoticia.EscreverCabecalho;
begin
  FFormato.DesenharCabecalho('data_atualizacao');
  FFormato.DesenharCabecalho('titulo');
  FFormato.DesenharCabecalho('conteudo');
  FFormato.DesenharCabecalho('sentimento');
end;

procedure TExportadorNoticia.ExportarDados(const Dados: TArray<TNoticia>);
var
  aNoticia: TNoticia;
begin
  EscreverCabecalho;
  for aNoticia in Dados do
  begin
    FFormato.PularLinha;
    FFormato.ExportarCampo(DateToStr(aNoticia.DataAtualizacao));
    FFormato.ExportarCampo(aNoticia.Titulo);
    FFormato.ExportarCampo(aNoticia.Conteudo);
    case aNoticia.Sentimento of
      senNegativo: FFormato.ExportarCampo('-1');
      senPositivo: FFormato.ExportarCampo('1');
      senNeutro: FFormato.ExportarCampo('0');
    end;
  end;
  FFormato.SalvarArquivo('dados\Noticias');
end;

end.
