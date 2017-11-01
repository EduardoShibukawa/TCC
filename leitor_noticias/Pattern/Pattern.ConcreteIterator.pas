unit Pattern.ConcreteIterator;

interface

uses
  Contnrs, Pattern.Iterator, Pattern.Aggregate, Model.Noticia;

type
  TConcreteIterator = class(TInterfacedObject, IIterator<TNoticia>)
  private
    FAggregate: IAggregate<TNoticia>;
    FIndice: integer;
  public
    constructor Create(Aggregate: IAggregate<TNoticia>);

    procedure PrimeiroObjeto;
    procedure ProximoObjeto;
    function ObjetoAtual: TNoticia;
    function FimLista: boolean;
    function Buscar(const Indice: integer): TNoticia;
  end;

implementation

uses
  System.Classes;

{ TConcreteIterator }

constructor TConcreteIterator.Create(Aggregate: IAggregate<TNoticia>);
begin
  FAggregate := Aggregate;
end;

function TConcreteIterator.Buscar(const Indice: integer): TNoticia;
begin
  Result := FAggregate.GetLista.Items[Indice];
end;

function TConcreteIterator.FimLista: boolean;
begin
  result := FIndice = Pred(FAggregate.GetLista.Count);
end;

function TConcreteIterator.ObjetoAtual: TNoticia;
begin
  result := FAggregate.GetLista.Items[FIndice];
end;

procedure TConcreteIterator.PrimeiroObjeto;
begin
  FIndice := 0;
end;

procedure TConcreteIterator.ProximoObjeto;
begin
  Inc(FIndice);
end;

end.
