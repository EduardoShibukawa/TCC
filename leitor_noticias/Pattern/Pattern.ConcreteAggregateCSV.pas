unit Pattern.ConcreteAggregateCSV;

interface

uses
  Pattern.Iterator, Pattern.Aggregate, Contnrs, System.Generics.Collections,
  Model.Noticia;

type
  { Concrete Aggregate }
  TConcreteAggregateCSV = class(TInterfacedObject, IAggregate<TNoticia>)
  private
    FLista: TObjectList<TNoticia>;

    function ToDate(SDate: string): TDate;
    function FormatString(AValue: String): String;

    procedure PreencherListaCSV(const CaminhoArquivo: string);
    procedure OrdenarLista;
  public
    constructor Create(const CaminhoArquivo: string);
    destructor Destroy; override;

    function GetLista: TObjectList<TNoticia>;
    function GetIterator: IIterator<TNoticia>;
  end;

implementation

uses
  System.Classes, System.SysUtils, Pattern.ConcreteIterator,
  System.DateUtils, System.JSON, Data.DBXJSON, System.Generics.Defaults;

{ TConcreteAggregateCSV }

constructor TConcreteAggregateCSV.Create(const CaminhoArquivo: string);
begin
  FLista := TObjectList<TNoticia>.Create;

  PreencherListaCSV(CaminhoArquivo);
  OrdenarLista;
end;

destructor TConcreteAggregateCSV.Destroy;
begin
  // Libera a lista de objetos da memória
  FLista.Free;
  inherited;
end;

function TConcreteAggregateCSV.FormatString(AValue: String): String;
begin
  Result := AValue.Replace('''', '').Replace('"', '').Trim;
end;

function TConcreteAggregateCSV.ToDate(SDate: string): TDate;
begin
  Result := EncodeDate(
    SDate.Substring(6, 4).ToInteger,
    SDate.Substring(3, 2).ToInteger,
    SDate.Substring(0, 2).ToInteger
  );
end;

function TConcreteAggregateCSV.GetIterator: IIterator<TNoticia>;
begin
  Result := TConcreteIterator.Create(Self);
end;

function TConcreteAggregateCSV.GetLista: TObjectList<TNoticia>;
begin
  Result := FLista;
end;

procedure TConcreteAggregateCSV.OrdenarLista;
var
  Comparison: TComparison<TNoticia>;
begin
  Comparison :=
    function(const Left, Right: TNoticia): Integer
    begin
      Result := CompareDate(Left.DataAtualizacao, Right.DataAtualizacao);
    end;

  FLista.Sort(TComparer<TNoticia>.Construct(Comparison));
end;

procedure TConcreteAggregateCSV.PreencherListaCSV(const CaminhoArquivo: string);
var
  aNoticia: TNoticia;
  aValores: TStringList;
  aValoresLinha: TStringList;
  aLine: String;

begin
  aValores := TStringList.Create;
  aValoresLinha := Tstringlist.Create;
  try
    aValoresLinha.Delimiter :=',';
    aValoresLinha.StrictDelimiter := True;

    aValores.LoadFromFile(CaminhoArquivo);
    for aLine in aValores.ToStringArray do
    begin
      if not aLine.Contains('data_atualizacao') then
      begin
        aValoresLinha.DelimitedText := aLine;
        aNoticia := TNoticia.Create;

        aNoticia.DataAtualizacao := ToDate(FormatString(aValoresLinha[0]));
        aNoticia.Titulo := FormatString(aValoresLinha[1]);
        aNoticia.Conteudo := FormatString(aValoresLinha[2]);
        if aValoresLinha.Count > 3 then
        begin
          if FormatString(aValoresLinha[3]) = '-1' then
            aNoticia.Sentimento := senNegativo
          else if FormatString(aValoresLinha[3])= '0' then
            aNoticia.Sentimento := senNeutro
          else aNoticia.Sentimento := senPositivo
        end
        else aNoticia.Sentimento := senNeutro;
        FLista.Add(aNoticia);
      end;
    end;
  finally
    aValores.Free;
  end;
end;


end.
