unit Pattern.ConcreteImplementorCSV;

interface

uses
  Classes, Pattern.Implementor;

type
  { Concrete Implementor }
  TFormatoCSV = class(TInterfacedObject, IFormato)
  private
    FCSVRow: TStrings;
    FLine: String;

    procedure SalvarLinha;
  public
    constructor Create;
    destructor Destroy; override;

    procedure PularLinha;
    procedure DesenharCabecalho(const Titulo: string);
    procedure ExportarCampo(const Valor: string);
    procedure SalvarArquivo(const NomeArquivo: string);
  end;

implementation

uses
  SysUtils, Forms, Windows, ShellAPI;

{ TFormatoHTML }

constructor TFormatoCSV.Create;
begin
  FCSVRow := TStringList.Create;
  FLine := String.Empty;
end;

procedure TFormatoCSV.DesenharCabecalho(const Titulo: string);
begin
  if not FLine.IsEmpty then
    FLine := FLine + ',';

  FLine := FLine + ' ' + QuotedStr(Titulo);
end;

destructor TFormatoCSV.Destroy;
begin
  FreeAndNil(FCSVRow);
  inherited;
end;

procedure TFormatoCSV.ExportarCampo(const Valor: string);
var
  aFormatedValue: String;
begin
  aFormatedValue := Valor.Replace(#$A, '');
  aFormatedValue := aFormatedValue.Replace(#$D, '');
  aFormatedValue := aFormatedValue.Replace(',', '');
  aFormatedValue := aFormatedValue.Replace('"', '');
  aFormatedValue := aFormatedValue.Replace('''', '');

  if not FLine.IsEmpty then
    FLine := FLine + ',';

  FLine := FLine + ' ' + QuotedStr(aFormatedValue);
end;

procedure TFormatoCSV.PularLinha;
begin
  SalvarLinha;
end;

procedure TFormatoCSV.SalvarArquivo(const NomeArquivo: string);
var
  CaminhoAplicacao: string;
  NomeCompleto: string;
begin
  CaminhoAplicacao := ExtractFilePath(Application.ExeName);
  NomeCompleto := Format('%s%s.csv', [CaminhoAplicacao, NomeArquivo]);
  DeleteFile(PWideChar(NomeCompleto));

  FCSVRow.SaveToFile(NomeCompleto);
  ShellExecute(0, nil, PChar(NomeCompleto), nil,  nil, SW_SHOWNORMAL);
end;

procedure TFormatoCSV.SalvarLinha;
begin
  FCSVRow.Add(FLine);
  FLine := String.Empty;
end;

end.

